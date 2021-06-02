import discord
from discord.utils import get
from discord.ext import commands
import requests
import json
import random
import asyncio


# TODO: arreglar el formato que trae los gif y que traiga diferetnes
# TODO: jumbo para agrandar los emotes
class Fun(commands.Cog):
    
    
    __slots__ = ('bot')
    
    def __init__(self, bot):
        self.bot = bot


    ### Comando say
    # hace decir al bot cualquier cosa

    @commands.command()
    async def say(self, ctx):
        embed = discord.Embed(title="Medi", description=f"{ctx.message.content[5:]}",color=0x7a78dd)
        embed.set_thumbnail(url="https://38.media.tumblr.com/05e2f169b5fc98ac8c6d0144ef7f62e0/tumblr_nodnrhCTN11qeq8xmo1_500.gif")
        await ctx.send(embed=embed)

    ### Comando ruleta
    # recibe una lista con las opciones de la ruleta y da una al azar

    @commands.command(pass_context=True)
    async def ruleta(self, ctx, message):

        embed = discord.Embed(title="Ruleta", description="Gira gira la ruleta, que caera?",color=0x7a78dd)
        embed.set_image(url="https://media.tenor.com/images/7b4d7b68511caaa6284a821c3506ac2c/tenor.gif")
        embed2 = discord.Embed(title="Ruleta", description="Tenemos un resultado",color=0x7a78dd)
        embed2.set_image(url="https://media.tenor.com/images/7b4d7b68511caaa6284a821c3506ac2c/tenor.gif")
        li = message.split(";")
        async with ctx.typing():
            msg = await ctx.send(embed=embed)
            embed2.set_footer(text=f"El resultado de la ruleta es: {random.choice(li)}")
            await asyncio.sleep(3)
        await msg.edit(embed=embed2)

    ### comando expand
    # HAce más grande un emote

    @commands.command()
    async def expand(self, ctx, emoji: discord.Emoji):
        await ctx.send(emoji.url)

    ### Comando Cry
    # envia un gif llorando
    #Todo: arreglar gif
    @commands.command()
    async def cry(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Ha empezado a llorar.**",inline=False)
        embed.set_image(url="https://img.17qq.com/images/eeatsrqx.jpeg")
        await ctx.send(embed=embed)
    
    ### Coamndo kiss
    # envia un beso a alguien

    #Todo: arreglar gif
    @commands.command()
    async def kiss(self, ctx, user: discord.Member = None):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        if user == None:
            embed.add_field(name=f"Medi:",value=f"**Ba..ba..baka!!! no me beses >//<.**",inline=False)
            embed.set_image(url="https://img.wattpad.com/3529d97de8e754120918bf801818306d3de04192/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f695146547548726c34506c4962513d3d2d3335353533353837372e313439613535633735356438656134653837333734373736323735352e676966")
        else:
            embed.add_field(name=f"{ctx.author}",value=f"**Ha besado a {user.mention}.**",inline=False)
            embed.set_image(url="https://media1.tenor.com/images/de80252a16557aad4ad9eeee836efeb1/tenor.gif?itemid=15882840")
        await ctx.send(embed=embed)

    ### Comando kill
    # Acabas con la vida de alguien

    #Todo: arreglar gif
    @commands.command()
    async def kill(self, ctx, user: discord.Member = None):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        if user == None:
            embed.add_field(name="Medi:",value=f"**Porque me haz matado QnQ... {ctx.author}**",inline=False)
            embed.set_image(url="https://k31.kn3.net/taringa/2/8/2/4/5/2/3/strongold_120/139.gif")
        else:
            embed.add_field(name=f"{ctx.author}",value=f"**Ha acabado con la vida de {user.mention}.**",inline=False)
            embed.set_image(url="https://k31.kn3.net/taringa/2/8/2/4/5/2/3/strongold_120/139.gif")
        await ctx.send(embed=embed)

    ### comando pat
    # acariacias a una persona
    #Todo: agregar gif
    @commands.command()
    async def pat(self, ctx, user: discord.Member = None):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        if user == None:
            embed.add_field(name="Medi:",value=f"**{ctx.author} gracias por acariciar mi cabeza.**",inline=False)
            embed.set_image(url="https://i.pinimg.com/originals/2e/27/d5/2e27d5d124bc2a62ddeb5dc9e7a73dd8.gif")
        else:
            embed.add_field(name=f"{ctx.author}",value=f"**Ha acariciado a {user.mention}.**",inline=False)
            embed.set_image(url="https://i.pinimg.com/originals/2e/27/d5/2e27d5d124bc2a62ddeb5dc9e7a73dd8.gif")
        await ctx.send(embed=embed)

    ### comando lick
    # lames a alguien, ¿porque lo harias?
    #Todo: agregar gif
    @commands.command()
    async def lick(self, ctx, user: discord.Member = None):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        if user == None:
            embed.add_field(name="Medi:",value=f"**{ctx.author} que haces?? eso no se hace conmigo QnQ.**",inline=False)
            embed.set_image(url="https://i.pinimg.com/originals/56/42/0d/56420de595681d55e4ea2cc9dcc48db9.gif")
        else:
            embed.add_field(name=f"{ctx.author}",value=f"**Esta lamiendo a {user.mention}, QUE ALGUIEN LO DETENGA!!.**",inline=False)
            embed.set_image(url="https://i557.photobucket.com/albums/ss19/mattkun_2009/Kanamemo-7-1-licking.gif")
        await ctx.send(embed=embed)

    ### comando bite
    # muerdes a una persona
    #Todo agregar gif
    @commands.command()
    async def bite(self, ctx, user: discord.Member = None):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        if user == None:
            embed.add_field(name="Medi:",value=f"**Eso duele {ctx.author}!** ",inline=False)
            embed.set_image(url="https://media1.tenor.com/images/d97e4bc853ed48bf83386664956d75ec/tenor.gif?itemid=10364764")
        else:
            embed.add_field(name=f"{ctx.author}",value=f"**Esta mordiendo a {user.mention}, que sigue? nadar con vagabundos?.**",inline=False)
            embed.set_image(url="https://media1.tenor.com/images/f308e2fe3f1b3a41754727f8629e5b56/tenor.gif?itemid=12390216")
        await ctx.send(embed=embed)

    ### comando happy
    # mandas un gif happy
    #Todo agregar gifs
    @commands.command()
    async def happy(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Esta que salta de la alegria.**",inline=False)
        embed.set_image(url="https://i.gifer.com/Vzg7.gif")
        await ctx.send(embed=embed)
    
    ### comando confused
    # mandas un gif confundido
    #Todo agregar gif
    @commands.command()
    async def confused(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Se encuentra confundido por alguna razon.**",inline=False)
        embed.set_image(url="https://media1.tenor.com/images/5e5507a6ec490f07864b86aff7e32852/tenor.gif?itemid=13802683")
        await ctx.send(embed=embed)
    
    ### comando boom
    # manda un gif explotando
    #Todo: agregar gif
    @commands.command()
    async def boom(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Ha explotado sin razon aparente.**",inline=False)
        embed.set_image(url="https://k36.kn3.net/taringa/2/1/2/2/7/1/57/demon3142/67D.gif?2085")
        await ctx.send(embed=embed)

    ### comando dance
    # manda un gif bailando
    #Todo: agregar gif
    @commands.command()
    async def dance(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Esta bailando un cumbion.**",inline=False)
        embed.set_image(url="https://i.pinimg.com/originals/69/53/22/695322e0b3edc81c6b2e0824962bb617.gif")
        await ctx.send(embed=embed)

    ### comando suicide
    # manda un gif suicidandoce
    #Todo: agregar gif
    @commands.command()
    async def suicide(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Esta cometiendo suicidio, es que no piensan en los niños?.**",inline=False)
        embed.set_image(url="https://cdn74.picsart.com/188863016000201.gif")
        await ctx.send(embed=embed)
    
    ### comando
    # manda un gif durmiendo
    #Todo: agregar gif
    @commands.command()
    async def sleep(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Se ha quedado dormido.**",inline=False)
        embed.set_image(url="https://media1.tenor.com/images/a7e8e8f9fd0a8784012d8f14b09da4a8/tenor.gif?itemid=12048209")
        await ctx.send(embed=embed)

    ### comando
    # manda un gif haciendo un dab
    #Todo: agregar gif
    @commands.command()
    async def dab(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Esta haciendo algo fuera de moda.**",inline=False)
        embed.set_image(url="https://media1.tenor.com/images/d13c16a8853e3b309db0ec7e573c4c94/tenor.gif?itemid=10617637")
        await ctx.send(embed=embed)

    ### comando 
    # manda un gif expresando simp
    #Todo: agregar gif
    @commands.command()
    async def simpatico(self, ctx):
        embed = discord.Embed(title="SIMP", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Es un SIMPatico más de la familia.**",inline=False)
        embed.set_image(url="https://media1.tenor.com/images/e604cf5467f0ec36f37ab56fc8575bb7/tenor.gif?itemid=18717773")
        await ctx.send(embed=embed)

    ### comando angry
    # manda un gif furioso
    #Todo: aggregar gif
    @commands.command()
    async def angry(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Esta furioso, salvece quien pueda!!!.**",inline=False)
        embed.set_image(url="https://i.pinimg.com/originals/fb/c7/5d/fbc75d7039be2f9a49bf11d3110d9c19.gif")
        await ctx.send(embed=embed)

    #Todo: aggregar gif
    @commands.command()
    async def tsundere(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Es una tsundere, no sabemos si es una linda, pero es lo que hay.**",inline=False)
        embed.set_image(url="https://img.wattpad.com/a27873451b0260b211798b3fa67e26e941795dbe/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f6f3236497a576e6e5361316762413d3d2d3231393132323031312e313439633661353666633132323162383438353636373737363932392e676966")
        await ctx.send(embed=embed)

    #Todo: aggregar gif
    @commands.command()
    async def fbi(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name="FBI",value=f"**ABRE LA PUERTA!! NOS INFORMARON DE UNAS LOLIS SECUESTRADAS. OPEN DE DOOR!!**",inline=False)
        embed.set_image(url="https://i.pinimg.com/originals/12/13/29/1213293a27c9f84df14051cf37510b41.gif")
        await ctx.send(embed=embed)

    #Todo: aggregar gif
    @commands.command()
    async def pucheros(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Esta haciendo pucheros?**",inline=False)
        embed.set_image(url="https://pa1.narvii.com/6469/b45ef85bb2226f4fa19964884a604c3d0a36930e_00.gif")
        await ctx.send(embed=embed)

    #Todo: aggregar gif
    @commands.command()
    async def run(self, ctx):
        embed = discord.Embed(title="", description="",color=0x7a78dd)
        embed.add_field(name=f"{ctx.author}",value=f"**Esta corriendo.**",inline=False)
        embed.set_image(url="https://i.pinimg.com/originals/0c/e8/be/0ce8bec2543d81ba65eefd309f0f0c5b.gif")
        await ctx.send(embed=embed)
    
    ### comando hug, manda un abrazo con un gif ramdon al miembre escrito

    @commands.command(pass_context=True)
    async def hug(self, ctx, user: discord.Member = None):

        apikey = "LIVDSRZULELA"  # test value
        lmt = 40
        search_term = "anime hug"
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

        if user == None:
            gifs = json.loads(r.content)
            link = gifs["results"][random.randint(0,len((gifs))-1)]["url"]
            await ctx.send(f"**{ctx.author} Estas solo? toma un abrazo mio**")
            await ctx.send(link)
        else:
            if r.status_code == 200:
                
                gifs = json.loads(r.content)
                link = gifs["results"][random.randint(0,len((gifs))-1)]["url"]
                await ctx.send(f"**{ctx.author} ha abrazado a {user.mention}**")
                await ctx.send(link)
            else:
                await ctx.send("No se encontro un gif", delete_after=12)

    @commands.command(pass_context=True)
    async def punch(self, ctx, user: discord.Member = None):

        apikey = "LIVDSRZULELA"  # test value
        lmt = 50
        search_term = "punch anime"
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

        if user == None:
            await ctx.send(f"**{ctx.author} No puedes golpear el aire**")
            
        else:
            if r.status_code == 200:
                
                gifs = json.loads(r.content)
                link = gifs["results"][random.randint(0,len((gifs))-1)]["url"]
                await ctx.send(f"**{ctx.author} ha golpeado a {user.mention} hasta la medula**")
                await ctx.send(link)
            else:
                await ctx.send("No se encontro un gif", delete_after=12)


    ### comando gif que trae un gif dado un tema

    @commands.command()
    async def gif(self, ctx):
        # set the apikey and limit
        apikey = "LIVDSRZULELA"  # test value
        lmt = 10

        # our test search
        search_term = ctx.message.content[4:]
        # get the top 8 GIFs for the search term
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
        if r.status_code == 200:
            # load the GIFs using the urls for the smaller GIF sizes
            top_8gifs = json.loads(r.content)
            await ctx.send(top_8gifs["results"][random.randint(0,len((top_8gifs))-1)]["url"])
        else:
            await ctx.send("No se encontro un gif", delete_after=12)


def setup(client):
    client.add_cog(Fun(client))