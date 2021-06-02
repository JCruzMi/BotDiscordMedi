import discord
import random
from discord.utils import get
from discord.ext import commands
class Info(commands.Cog):
    
    __slots__ = ('bot')

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs de info listos")

    ### Comando info para obtener la informacion de un usuario

    @commands.command()
    async def avatar(self, ctx, user: discord.Member = None):
        embed = discord.Embed()
        if user == None:
            user = ctx.author
            embed.set_image(url=f"{user.avatar_url}")
        else:
            embed.set_image(url=f"{user.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def info(self, ctx, user: discord.Member):
        rant = random.randint(1, 255)

        user = user or ctx.author

        embed = discord.Embed(title="{}'s info".format(user.name), description="Esto es lo que encontre de {}!".format(user.name), color=rant)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Name", value=user.name, inline=False) #Gives the username without the @ and #
        embed.add_field(name="ID", value=user.id, inline=False) #Give id of the user you tagged
        embed.add_field(name="Status", value=user.status, inline=False) #Gives status of the user. online, dnd, offline, etc.
        embed.add_field(name="Highest role", value=user.top_role, inline=False) #Tells you the highest role of that user.
        embed.add_field(name="Joined", value=user.joined_at, inline=False) #Give you the date and time the user joined.
        await ctx.send(embed=embed)

    ### comando  que trae la info del server
    
    @commands.command(name="server_info")
    async def server_info(self, ctx):

        embed = discord.Embed(title="Información del servidor",colour=ctx.guild.owner.colour)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        
        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
        
        fields = [("ID", ctx.guild.id, False),
        ("Dueño", ctx.guild.owner, False),
        ("Región", ctx.guild.region, False),
        ("Miembros", len(ctx.guild.members), True),
        ("Humanos", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
        ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
        ("Baneados", len(await ctx.guild.bans()), True),
        ("Estados", f"🟢 {statuses[0]}    🟠 {statuses[1]}    🔴 {statuses[2]}    ⚪ {statuses[3]}   ", False),
        ("Canales de texto", len(ctx.guild.text_channels), True),
        ("Canales de voz", len(ctx.guild.voice_channels), True),
        ("Categorias", len(ctx.guild.categories), True),
        ("Roles", len(ctx.guild.roles), True),
        ("Invitaciones", len(await ctx.guild.invites()), True),
        ("Creado en", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), False)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
            
        await ctx.send(embed=embed)

    #Info roles
    @commands.command(name="roles_info")
    async def roles_info(self, ctx):

        embed = discord.Embed(title="Información de roles",colour=ctx.guild.owner.colour)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        info = {}

        for rol in list(ctx.guild.roles):
            info[rol] = 0

        for member in ctx.guild.members:
            for role in member.roles:
                info[role] += 1
        
        print(info)
        for i in info:
            embed.add_field(name=i, value=f"personas con este rol: {info[i]}", inline=True)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Info(client))