import discord
from discord.ext import commands
import asyncio
import random
import json
import os

class Tic(commands.Cog):
    
    __slots__ = ('bot')

    def __init__(self, bot):
        self.bot = bot
        self.condicionGanar = [
            [0,1,2],
            [3,4,5],
            [6,7,8],
            [0,3,6],
            [1,4,7],
            [2,5,8],
            [0,4,8],
            [2,4,6]
        ]
        self.turn = ""
        self.tablero = []
        self.count = 0 
        self.p1 = ""
        self.p2 = ""
        self.gameOver = True


    @commands.Cog.listener()
    async def on_ready(self):
        
        print("Cogs de tres el raya listos")
    
    @commands.command()
    async def vs(self, ctx, p1 : discord.Member, p2 : discord.Member):

        guild = ctx.message.guild.id

        if self.gameOver:
            self.tablero = [":white_large_square:",":white_large_square:",":white_large_square:",
                        ":white_large_square:",":white_large_square:",":white_large_square:",
                        ":white_large_square:",":white_large_square:",":white_large_square:"]
            self.turn = ""
            self.gameOver = False
            self.count = 0

            self.p1 = p1
            self.p2 = p2

            line = ""
            for x in range(len(self.tablero)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + self.tablero[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + self.tablero[x]
            
            num = random.randint(1, 2)
            if num == 1:
                self.turn = self.p1
                await ctx.send(f"Es el turno de {self.p1.mention}")
            else:
                self.turn = self.p2
                await ctx.send(f"Es el turno de {self.p2.mention}")
        else:
            await ctx.send(f"Ya hay un juego en progreso. {self.p1} {self.p2} {self.gameOver}")


    @commands.command()
    async def trfin(self, ctx):

        guild = ctx.message.guild.id    

        if ctx.author == self.p1 or ctx.author == self.p2:
            await ctx.send(f"{ctx.author} ha terminado el juego.")
            self.turn = ""
            self.p1 = ""
            self.p2 = ""
            self.tablero = []
            self.count = 0
            self.gameOver = True
        else:
            await ctx.send("No puedes para un juego que no es tuyo.")

    @commands.command()
    async def trplay(self, ctx, pos: int):

        if not self.gameOver:
            mark = ""
            if self.turn == ctx.author:
                if self.turn == self.p1:
                    mark = ":regional_indicator_x:"
                elif self.turn == self.p2:
                    mark = ":o2:"
                if 0 < pos <10 and self.tablero[pos - 1] == ":white_large_square:":
                    self.tablero[pos - 1] = mark
                    self.count += 1

                    # Impirmir tablero

                    line = ""
                    for x in range(len(self.tablero)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + self.tablero[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + self.tablero[x]

                    #verificar si alguein gano
                    for condicion in self.condicionGanar:
                        if self.tablero[condicion[0]] == mark and self.tablero[condicion[1]] == mark and self.tablero[condicion[2]] == mark:
                            self.gameOver = True


                    if self.gameOver:
                        await ctx.send(f"Ha ganado {mark}.")
                    elif self.count >= 9:
                        await ctx.send("Ha sido un empate.")
                        self.gameOver = True

                    # cambir turnos

                    if self.turn == self.p1:
                        self.turn = self.p2
                    elif self.turn == self.p2:
                        self.turn = self.p1

                else:
                    await ctx.send(f"Asegurate de introducir una posicion valida y que no este ya ocupada.")
                    
            else:
                await ctx.send(f"No es tu turno aun {ctx.author.mention}.")
        else:
            await ctx.send("Porfavor inicien un juego antes con el comando &tres.")


def setup(client):
    client.add_cog(Tic(client))