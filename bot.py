import discord
from discord.utils import get
import aiofiles
import os
import random
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands, tasks
from itertools import cycle
import requests
import json
import shutil
import asyncio
import sys


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True

status = cycle(['Music','Fun','Admin','&help'])

# Leer el Token de la carpeta data
TokenFile = open("./data/Token.txt", "r")
TOKEN = TokenFile.read() 

OWNERID = 214361684922466304

# Definimos el "bot"
bot = commands.Bot(command_prefix = "&", case_insensitive=True, intents=intents, help_command=None)

class BotData:
    def __init__(self):
        self.welcome_channel = None
        self.goodbye_channel = None
    
botdata = BotData()

# Evento para saber si el bot s inicio correctamente
@bot.event
async def on_ready():
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song || &help"))
    change_status.start()


    # Archivos con los datos de las reacciones_roles
    bot.reaction_roles = []

    for file in ["./reaction_roles.text"]:
        async with aiofiles.open(file, mode="a") as temp:
            pass
            
    async with aiofiles.open("reaction_roles.text", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))

    
    print("Bot listo")
    if not os.path.exists('my_folder'):
        depure.start()

### Reaccionar y dar rol o on_rew_reaction_add
# añade el rol al reaccionar

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Streaming(name=(next(status)), url="https://www.twitch.tv/huan_mura_to"))

@tasks.loop(seconds=1600)
async def depure():
    mydir = "downloads"
    try:
        shutil.rmtree(mydir)
        print("eliminando canciones")
    except OSError as e:
        print(e)
        print("no existe el folder")

@bot.event
async def on_raw_reaction_add(payload):
    for role_id, msg_id, emoji in bot.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(role_id))
            return

### Reaccionar y quitar rol o on_rew_reaction_add
# remueve el rol al reaccionar

@bot.event
async def on_raw_reaction_remove(payload):
    for role_id, msg_id, emoji in bot.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            guild = bot.get_guild(payload.guild_id)
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))
            return

### Comando para añadir un rol a una reaccion

@bot.command()
async def react_to(ctx, role: discord.Role=None, msg: discord.Message=None, emoji=None):
    if role != None and msg != None and emoji != None:
        await msg.add_reaction(emoji)
        bot.reaction_roles.append((role.id, msg.id, str(emoji.encode("utf-8"))))

        async with aiofiles.open("reaction_roles.text", mode="a") as file:
            emoji_utf =  str(emoji.encode("utf-8"))
            await file.write(f"{role.id} {msg.id} {emoji_utf}\n")

        await ctx.channel.send("Se ha puesto una reacción")

    else:
        await ctx.channel.send("Argumentos invalidos")


### Obtiene errores y los dice

@bot.event 
async def on_command_error(ctx,error):
    embed = discord.Embed(
    title='',
    color=discord.Color.red())
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.MissingPermissions):
        embed.add_field(name=f'Permisos invalidos', value=f'No tienes {error.missing_perms} permisos.')
        await ctx.send(embed=embed)
    else:
        embed.add_field(name = f':x: Error terminal', value = f"```{error}```")
        await ctx.send(embed = embed)
        raise error

# ------------------------------Trae todos los cogs--------------------------------------------------

# Habilita las funciones Cog

@bot.command()
async def load(ctx, extension):
    # Verifica si el usuario es el creador del bot
    if ctx.author.id == OWNERID:
        bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Habilitamos todooo!")
    else:
        await ctx.send(f"No eres lo sufientemente cool para usar este comando")

# Desabilita los comandos Cog

@bot.command()
async def unload(ctx, extension):
    # Verifica si el usaurio es el creador del bot
    if ctx.author.id == OWNERID:
        bot.unload_extension(f'Cogs.{extension}')
        await ctx.send(f"Desabilitando comandos de admin!")
    else:
        await ctx.send(f"No eres lo sufientemente cool para usar este comando")

# Reload command to manage our "Cogs" or extensions

@bot.command(name = "reload")
async def reload_(ctx, extension):
    if ctx.author.id == OWNERID:
        bot.reload_extension(f'Cogs.{extension}')
        await ctx.send(f"Recargando cogs!") 
    else:
        await ctx.send(f"No eres lo suficientemente cool para este comando")

# # Automaticamante carga todos los archivos .py de Cogs
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'Cogs.{filename[:-3]}')
        except Exception:
            raise Exception



# Run our bot
bot.run(str(TOKEN)) # Make sure you paste the CORRECT token in the "./data/Token.txt" file