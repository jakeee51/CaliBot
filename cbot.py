# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: PokeBot
Functionality Purpose: A Pokemon game for Discord
Version: Beta
'''
RELEASE = "v0.0.2 - 9/6/20"

from key import bot_pass, cwd
from pokebot import *
from cea import *
from gym import *
from config import *
from tools import *

token = bot_pass()
os.chdir(cwd)


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)
sys.stdout = Unbuffered(sys.stdout)

@bot.event
async def on_ready():
    await bot.change_presence(activity = Game(name = "/help (For all cmds)"))
    print("We have logged into {0.user}".format(bot))

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return -1;

    # General CaliBot Commands
    if ctx.content.startswith('/help'): # Help command
        with open("cmds.md") as f:
            cmds = f.read()
        await ctx.channel.send("__**CaliBot Commands:**__```CSS\n" + cmds + "```")
    await bot.process_commands(ctx)


if __name__ == "__main__":
    bot.run(token)
##bot.logout()
##bot.close()
##print("We have logged out of bot bot")
