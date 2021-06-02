import discord
from discord.ext import commands
import os
import shutil
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL



ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(f'```ini\n[Añadiendo {data["title"]} a la cola.]\n```', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer(commands.Cog):

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'vol', 'del')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(120):  # 3 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'Procesando la canción.\n'
                                             f'```css\n[{e}]\n```',)
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed = discord.Embed(title="Reproduciendo", description=f"{source.title}", color=0x7a78dd)
            embed.add_field(name="mandada por", value=f"{source.requester}", inline=False)
            self.np = await self._channel.send(embed=embed, delete_after=60)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()

            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs musica listos")

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('No puedes usar este comando.', delete_after=20)
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            embed = discord.Embed(title="Medi", description=f"{'Por favor verifica que estes en un canal valido'}")
            embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/96105795498170735/3045F38DAF1EAFF1D09EF6CF2E8D5E4F0E36D8CF/")
            await ctx.send(embed=embed, delete_after=20)

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='connect', aliases=['join'])
    async def connect_(self, ctx):
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            raise InvalidVoiceChannel('No te haz conectado a ningun canal aun.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moviendo al canal: <{channel}>.', delete_after=20)
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moviendo al canal: <{channel}>.', delete_after=20)
        
        embed = discord.Embed(title="Medi", description=f'Conectando a: **{channel}**',)
        embed.set_thumbnail(url="https://i.pinimg.com/originals/c3/76/01/c376012492fdf168beb84037d74b2587.gif")
        await ctx.send(embed=embed, delete_after=20)

    @commands.command(name='play', aliases=['sing','p'])
    async def play_(self, ctx, *, search: str):
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=True)

        await player.queue.put(source)

    @commands.command(name='pause')
    async def pause_(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            embed = discord.Embed(title="Actualmente no estoy reproduciendo nada!")
            embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/96105795498170735/3045F38DAF1EAFF1D09EF6CF2E8D5E4F0E36D8CF/")
            return await ctx.send(embed=embed, delete_after=20)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f'**`{ctx.author}`**: Cancion pausada!', delete_after=20)

    @commands.command(name='resume')
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="Actualmente no estoy reproduciendo nada!")
            embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/96105795498170735/3045F38DAF1EAFF1D09EF6CF2E8D5E4F0E36D8CF/")
            return await ctx.send(embed=embed, delete_after=20)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f'**`{ctx.author}`**: Reanudando canción!')

    @commands.command(name='skip')
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="Actualmente no estoy reproduciendo nada!")
            embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/96105795498170735/3045F38DAF1EAFF1D09EF6CF2E8D5E4F0E36D8CF/")
            return await ctx.send(embed=embed, delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f'**`{ctx.author}`**: Ha adelantado la playlist!',delete_after=20)

    @commands.command(name='queue', aliases=['q', 'playlist'])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('Actualmente no estas conectado a nincun canal de voz', delete_after=15)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('Actualmente no hay más canciones en cola', delete_after=15)

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(title=f'Proximas canciones {len(upcoming)}', description=fmt)

        await ctx.send(embed=embed, delete_after=40)

    @commands.command(name='now_playing', aliases=['np', 'current', 'playing'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="Actualmente no estas conectado en ningun canal valido!",delete_after=20)
            embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/96105795498170735/3045F38DAF1EAFF1D09EF6CF2E8D5E4F0E36D8CF/")
            return await ctx.send(embed=embed, delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            embed = discord.Embed(title="Actualmente no estoy reproduciendo ninguna canción!",delete_after=20)
            embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/96105795498170735/3045F38DAF1EAFF1D09EF6CF2E8D5E4F0E36D8CF/")
            return await ctx.send(embed=embed, delete_after=20)

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send(f'**Esta sonando:** `{vc.source.title}` '
                                   f'puesta por `{vc.source.requester}`')

    @commands.command(name='stop', aliases=['leave','l'])
    async def stop_(self, ctx):
        
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="Actualmente no estoy reproduciendo nada!", delete_after=20)
            embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/96105795498170735/3045F38DAF1EAFF1D09EF6CF2E8D5E4F0E36D8CF/")
            return await ctx.send(embed=embed, delete_after=20)

        await self.cleanup(ctx.guild)
    
    @commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol: float):
        
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('No estoy actualmente en ningun canal de voz', delete_after=20)

        if not 0 < vol < 101:
            return await ctx.send('Porfavor ponga un valor de 1 entre 100', delete_after=20)

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f'**`{ctx.author}`**: Volumen en **{vol}%**', delete_after=20)



def setup(client):
    client.add_cog(Music(client))
