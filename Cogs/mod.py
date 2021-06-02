import discord
from discord.utils import get
from discord.ext import commands, tasks
import requests
import json
import PIL
from PIL import Image
from io import BytesIO
import os

class Mod(commands.Cog):
    
    __slots__ = ('bot','_guild')

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        
        print("Cogs de mod listos")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.command(name="create_emoji",aliases=['cre'])
    async def create_emoji(self, ctx, object, *, name):
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            r = requests.get(object)
            img = Image.open(BytesIO(r.content), mode='r')
            try:
                img.seek(1)

            except EOFError:
                is_animated = False

            else:
                is_animated = True

            if is_animated == True:
                await ctx.send("No puede poner gif")

            elif is_animated == False:
                b = BytesIO()
                img.save(b, format='PNG')
                b_value = b.getvalue()
                emoji = await guild.create_custom_emoji(image=b_value, name=name)
                await ctx.send(f'se ha subido el emote: <:{name}:{emoji.id}>')

    #ToDo: pasar los cocmandos de moderación de bot.py a mod.py

    


def setup(client):
    client.add_cog(Mod(client))