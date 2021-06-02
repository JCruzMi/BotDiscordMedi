import discord
from discord.utils import get
import aiofiles
import os
import asyncio
import sys
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands, tasks

class Wel_Bye(commands.Cog):
    
    __slots__ = ('bot','_guild')

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):

        commands.welcome_channels = {}
        commands.goodbye_channels = {}

        for file in ["./welcome_channels.text", "./goodbye_channels.text"]:
            async with aiofiles.open(file, mode="a") as temp:
                pass


        async with aiofiles.open("./welcome_channels.text", mode="r") as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split(" ")
                commands.welcome_channels[int(data[0])] = (int(data[1]), " ".join(data[2:]).strip("\n"))
            
        async with aiofiles.open("./goodbye_channels.text", mode="r") as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split(" ")
                commands.goodbye_channels[int(data[0])] = (int(data[1]), " ".join(data[2:]).strip("\n"))

        print("Cogs de wel_bye listos")

        ### comando que permite seleccionar un canal para dar el mensaje de bienvenida
    # recibe y guarda el canal y el mensaje

    @commands.command(name="set_welcome_channel", aliases=['swc'])
    @has_permissions(manage_roles=True, ban_members=True)
    async def set_welcome_channel(self, ctx, new_channel: discord.TextChannel= None,* , message = None):
        if new_channel != None and message != None:
            for channel in ctx.guild.channels:
                if channel == new_channel:
                    commands.welcome_channels[ctx.guild.id] = (channel.id, message)
                    await ctx.channel.send(f"Canal de bienvenida se ha establecido en **{channel.name}** con el mensaje **{message}**", delete_after=15)
                    await channel.send("Este es nuevo canal de bienvenida", delete_after=15)

                    async with aiofiles.open("welcome_channels.text", mode="a") as file:
                        await file.write(f"{ctx.guild.id} {new_channel.id} {message}\n")
                    
                    return
            await ctx.channel.send("no se puedo encontrar el canal dado", delete_after=15)               
        else:
            await ctx.channel.send("No tienes incluido un canal de bienvenida.", delete_after=15)

    ### comando que permite seleccionar un canal para dar el mensaje de despedida
    # recibe y guarda el canal y el mensaje

    @commands.command(name="set_goodbye_channel", aliases=['sgc'])
    @has_permissions(manage_roles=True, ban_members=True)
    async def set_goodbye_channel(self, ctx, new_channel: discord.TextChannel= None,* , message = None):
        if new_channel != None and message != None:
            for channel in ctx.guild.channels:
                if channel == new_channel:
                    commands.goodbye_channels[ctx.guild.id] = (channel.id, message)
                    await ctx.channel.send(f"Canal de despedida se ha establecido en **{channel.name}** con el mensaje **{message}**", delete_after=15)
                    await channel.send("Este es nuevo canal de despedidas", delete_after=15)

                    async with aiofiles.open("goodbye_channels.text", mode="a") as file:
                        await file.write(f"{ctx.guild.id} {new_channel.id} {message}\n")
                    
                    return
            await ctx.channel.send("no se puedo encontrar el canal dado", delete_after=15)               
        else:
            await ctx.channel.send("No tienes incluido un canal de despedida.", delete_after=15)

    ### evento que se ejecuta al unirse un nuevo miembro al servidor

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for guild_id in commands.welcome_channels:
            if guild_id == member.guild.id:
                channel_id, message = commands.welcome_channels[guild_id]
                embed = discord.Embed(title="Bienvenid@", description=f"{message} {member.mention}",color=0x7a78dd)
                embed.set_thumbnail(url="https://media1.tenor.com/images/7fc329273e705d450ba1b73ef92444f2/tenor.gif?itemid=9658069")
                await self.bot.get_guild(guild_id).get_channel(channel_id).send(embed=embed)
                
                # ToDo: arreglar para poder elegir el rol que obtiene al ingresar un nuevo miembro
                

    ### evento que se ejecuta al irse un miembro

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        for guild_id in commands.goodbye_channels:
            if guild_id == member.guild.id:
                channel_id, message = commands.goodbye_channels[guild_id]
                embed = discord.Embed(title="Hasta luego QnQ", description=f"{message} {member.mention}",color=0x7a78dd)
                embed.set_thumbnail(url="https://pa1.narvii.com/6581/eae525c065e8d03c4266c6b12c5ca3c9841f218c_hq.gif")
                await self.bot.get_guild(guild_id).get_channel(channel_id).send(embed=embed)
                return





def setup(client):
    client.add_cog(Wel_Bye(client))