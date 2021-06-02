import discord
from discord.ext import commands
import asyncio

# TODO: Comando Ruleta, Comando Punch, Comando set_role 

class Help(commands.Cog):
    
    __slots__ = ('bot')

    def __init__(self, bot):
        self.bot = bot
    #pagina 1
    page1 = discord.Embed(title="Comandos Extra", descripción="Comanos para todos divertirse.", colour=discord.Colour.orange())

    page1.add_field(name="&say", value="*Descripción: Haces hablar al bot con un mensaje tuyo.* \n" "`&say`\n" "Uso: `&say <mensaje>`", inline=False)
    page1.add_field(name="&gif", value="*Descripción: Muestra un gif con la tematica dada.* \n" "`&gif` \n" "Uso: `&gif <tematica>`", inline=False)
    page1.add_field(name="&ruleta", value="*Descripción: Crea una ruleta para jugar con otros.* \n" "`&ruleta` \n" "Uso: `&ruleta <tema1;tema2;tema3;etc>`", inline=False)
    page1.add_field(name="&expand", value="*Descripción: Hace el emote más grande* \n" "`&expand` \n" "Uso: `&expand <emote creado>`")


    #pagina 11
    page11 = discord.Embed(title="Comandos interactivos 1", descripción="Comanos para interactuar.", colour=discord.Colour.orange())

    page11.add_field(name="&hug", value="*Descripción: Mandas un abrazo a alguien.* \n" "`&hug` \n" "Uso: `&hug <usuario>`", inline=False)
    page11.add_field(name="&punch", value="*Descripción: Mandas un golpe a tus enemigos más odiados.* \n" "`&punch` \n" "Uso: `&punch <usuario>`", inline=False)
    page11.add_field(name="&kiss", value="*Descripción: Besas a una persona de tu elección.* \n" "`&kiss` \n" "Uso: `&kiss <usuario>`", inline=False)
    page11.add_field(name="&kill", value="*Descripción: Acabas con la vida de una persona.* \n" "`&kill` \n" "Uso: `&kill <usuario>`", inline=False)
    page11.add_field(name="&pat", value="*Descripción: Acariacias a alguien.* \n" "`&pat` \n" "Uso: `&pat <usuario>`", inline=False)
    page11.add_field(name="&lick", value="*Descripción: Lames a alguien, ¿porque lo harias?.* \n" "`&lick` \n" "Uso: `&lick <usuario>`", inline=False)
    page11.add_field(name="&bite", value="*Descripción: Muerdes a una persona.* \n" "`&bite` \n" "Uso: `&bite <usuario>`", inline=False)
    
    # pagina 12
    page12 = discord.Embed(title="Comandos interactivos 2", descripción="Comandos para expresar algo.", colour=discord.Colour.orange())

    page12.add_field(name="&boom", value="*Descripción: Mandas un gif explotando.* \n " "`&boom`",inline=False)
    page12.add_field(name="&dance", value="*Descripción: Mandas un gif bailando.* \n " "`&dance`",inline=False)
    page12.add_field(name="&suicide", value="*Descripción: Mandas un gif suicidandote.* \n " "`&suicide`",inline=False)
    page12.add_field(name="&sleep", value="*Descripción: Mandas un gif durmiendo.* \n " "`&sleep`",inline=False)
    page12.add_field(name="&dab", value="*Descripción: Mandas un gif haciendo un dab.* \n " "`&dab`",inline=False)
    page12.add_field(name="&simpatico", value="*Descripción: Mandas un gif siendo Simp.* \n " "`&simpatico`",inline=False)
    page12.add_field(name="&angry", value="*Descripción: Mandas un gif de enojo.* \n " "`&angry`",inline=False)
    page12.add_field(name="&tsundere", value="*Descripción: Mandas un gif siendo tsundere.* \n " "`&tsundere`",inline=False)
    page12.add_field(name="&fbi", value="*Descripción: Mandas un gif FBI.* \n " "`&fbi`",inline=False)
    page12.add_field(name="&pucheros", value="*Descripción: Mandas un gif haciendo pucheros.* \n " "`&pucheros`",inline=False)
    page12.add_field(name="&run", value="*Descripción: Mandas un gif corriendo,* \n " "`&run`",inline=False)
    page12.add_field(name="&happy", value="*Descripción: Mandas un gif de felicidad.* \n" "`&happy`", inline=False)
    page12.add_field(name="&confused", value="*Descripción: Mandas un gif de confusion.* \n" "`&confused`", inline=False)
    page12.add_field(name="&cry", value="*Descripción: Manda un gif llorando.* \n" "`&cry`", inline=False)



    #pagina2
    page2 = discord.Embed(title="Comandos musica", descripción="Comandos para musica.", colour=discord.Colour.orange())

    page2.add_field(name="&play", value="*Descripción: Reproduce una canción.*\n" "`&play` o `&sing` o `&p` \n" "Uso: `&play <nombre o link>`", inline=False)
    page2.add_field(name="&pause", value="*Descripción: Pausa la canción que suena actualmente.*\n" "`&pause`", inline=False)
    page2.add_field(name="&resume", value="*Descripción: Reanuda la cancíon pausada.*\n" "`&resume`", inline=False)
    page2.add_field(name="&skip", value="*Descripción: Salta la canción actual.*\n""`&skip`", inline=False)
    page2.add_field(name="&now_playing", value="*Descripción: Da información de la canción actual.*\n" "`&now_playing` o `&np` o `&current` o `&playing`", inline=False)
    page2.add_field(name="&queue", value="*Descripción: Muestra una lista de las proximas canciones.*\n" "`&q` o `queue` o `playlist`", inline=False)
    page2.add_field(name="&volume", value="*Descripción: Cambia el volumen de la musica*\n" "`&vol` o `vol` \n" "Uso: `&vol <valor entre 1 y 100>`", inline=False)
    page2.add_field(name="&stop", value="*Descripción: Elimina la musica y al bot.*\n" "`&stop` `&l` `&leave`", inline=False)

    #pagina 3
    page3 = discord.Embed(title="Comandos para moderadores", descripción="Comanos para moderadores.", colour=discord.Colour.orange())

    page3.add_field(name="&set_welcome_channel", value="*Descripción: Selecciona un canal para saludar a los nuevos usuarios.*\n" "`&set_welcome_channel` o `swc`\n" "Uso: `&set_welcome_channel <canal> <mensaje>`", inline=False)
    page3.add_field(name="&set_goodbye_channel", value="*Descripción: Selecciona un canal para despedirte.*\n" "`&set_goodbye_channel` o `sgc` \n" "Uso: `&set_godbue_channel <canal> <mensaje>`", inline=False)
    page3.add_field(name="&create_emoji", value="*Descripción: Crea un emote para el server.*\n" "`&create_emoji` o `cre` \n" "Uso: `&create_emoji <link> <nombre>`", inline=False)
    page3.add_field(name="&react_to", value="*Descripción: Pone un rol a un reacción en un texto.*\n" "`&react_to` \n" "Uso: `&react_to <Rol> <msj id> <emoji>`", inline=False)

    #pagina 4
    page4 = discord.Embed(title="Comandos de información", descripción="Comandos para información.", colour=discord.Colour.orange())
    
    page4.add_field(name="&help", value="*Descripción: Muestra los comandos.* \n" "`&help` \n" "Uso : `&help <número de hoja opcional>`", inline=False)
    page4.add_field(name="&info", value="*Descripción: Muestra la información de alguien.* \n" "`&info` \n" "Uso: `&info <usuario o id_usuario>`", inline=False)
    page4.add_field(name="&roles_info", value="*Descripción: Muestra la información de los roles.* \n" "`&roles_info`", inline=False)
    page4.add_field(name="&server_info", value="*Descripción: Muestra la información del servidor.* \n" "`&server_info`" , inline=False)
    page4.add_field(name="&avatar", value="*Descripción: Muestra el avatar del usuario.* \n" "`&avatar`" "Uso: `&avatar <usuariou>`", inline=False)
    
    #page 5

    page5 = discord.Embed(title="Comandos de tres en raya", descripción="Comandos para una partida de 3 en raya.", colour=discord.Colour.orange())

    page5.add_field(name="&vs", value="*Descripción: Crea una partida de 3 en raya.* \n" "`&vs`", inline=False)
    page5.add_field(name="&trplay", value="*Descripción: Selecciona una casilla del tablero.* \n" "`&trplay` \ns" "Uso: `&trplay <numero del 1-9>`", inline=False)
    page5.add_field(name="&trfin", value="*Descripción: Termina la partida.* \n" "`&trfin`", inline=False)


    commands.help_pages = [page11,page12,page2,page3,page4,page5,page1]
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs de Help listos")

    

    ### comando help muestra todos los comandos

    @commands.command(pass_context=True)
    async def help(self, ctx, msg=None):
        if msg == "1" or msg == "2" or msg == "3" or msg == "4" or msg == "5" or msg == "6" or msg == "7":
            current = int(msg)-1
        else:
            current= 0
        buttons = [u"\u23EA",u"\u25C0",u"\u25B6",u"\u23E9"]
        msg = await ctx.send(embed=commands.help_pages[current])

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check = lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60)
            
            except asyncio.TimeoutError:
                embed = commands.help_pages[current]
                embed.set_footer(text="Tiempo excedido.")
                await msg.clear_reactions()
            else:
                previous_page = current

                if reaction.emoji == u"\u23EA":
                    current = 0
                elif reaction.emoji == u"\u25C0":
                    if current > 0:
                        current -= 1
                elif reaction.emoji == u"\u25B6":
                    if current < len(commands.help_pages)-1:
                        current += 1
                elif reaction.emoji == u"\u23E9":
                    current = len(commands.help_pages)-1
                
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)
                
                if current != previous_page:
                    await msg.edit(embed=commands.help_pages[current])

    
    
    
def setup(client):
    client.add_cog(Help(client))