# -*- coding: utf-8 -*-

from discord.ext import commands
from discord import Game
from discord import Embed
import asyncio
from tools import *

bot = commands.Bot(command_prefix='/', help_command=None)

@bot.command()
async def pokebot(ctx, arg):
    if "Cali#6919" == str(ctx.author):
        if arg == "start":
            with open("states/channels.txt", 'a') as f:
                f.write(str(ctx.channel.id) + '\n')
            await ctx.channel.send("`Pokebot game has started! Pokemon will now spawn in this channel!`")
        elif arg == "stop":
            edit_file("states/channels.txt", str(ctx.channel.id))
            await ctx.channel.send("`Pokebot game has stopped! Pokemon will stop spawning in this channel!`")
        else:
            await ctx.channel.send("`Invalid Pokebot command!`")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error