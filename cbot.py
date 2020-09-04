# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: PokeBot
Functionality Purpose: A Pokemon game for Discord
Version: 
'''
RELEASE = "v0.0.1 - 9/4/20"

import discord
import asyncio
import re, os, sys, time, json, smtplib, datetime
from key import bot_pass, cwd
from config import *
from tools import *
try:
    import GeoLiberator as GL
except ModuleNotFoundError:
    pass
token = bot_pass()
os.chdir(cwd)
RUN_TIME = datetime.datetime.now()
LAST_MODIFIED = RUN_TIME.strftime("%m/%d/%Y %I:%M %p")

'''
from discord.ext import commands
bot = commands.Bot("!")
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
'''

#Organize code
#Have `/verify` prompt to specify college

#Prevent email from spam

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
        return getattr(self .stream, attr)
sys.stdout = Unbuffered(sys.stdout)

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "/help (For all cmds)"))
    print("We have logged in as {0.user}".format(client))

'''@client.event
async def on_member_join(member):
    #await client.edit_message(message_var, "This is the edit to replace the message.")
    channel = client.get_channel(brothers.general)
    await asyncio.sleep(15)
    await channel.send("__***Welcome to the NJIT MSA Discord Server!***__\n\n**Please type `/verify <YOUR_NJIT_UCID>` to join the chat.**")'''

@client.event
async def on_reaction_add(reaction, user):
    pass

@client.event
async def on_reaction_remove(reaction, user):
    pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return -1;
    if message.content == 'nu u':
        if "Cali#6919" == str(message.author):
            await message.channel.send("nu u!")
    if message.content.lower().startswith('/version'):
        if "Cali#6919" == str(message.author):
            await message.channel.send(f"`{RELEASE} | {LAST_MODIFIED}`")
    if re.search("(nu nu|Nunu|nunu)", message.content): # Taha
        if message.author.id == 496079190475538461:
            await message.channel.send("nu nu?")
    if "/taha" in message.content.lower(): # Taha
        if message.author.id == 496079190475538461:
            await message.channel.send("Yes we can")
    if "/anas" in message.content.lower(): # Anas
        if message.author.id == 406821958563528737:
            await message.channel.send("knowimsayin dawg", delete_after=10)
    if "Solo Leveling" in message.content:          
        if message.author.id == 185842527520292874: # Omar E.
            await message.channel.send("Yo that junk is fire :fire:", delete_after=10)
    if "ws" == message.content:
        await message.channel.send("Walaikumu Salam")
    if "texas" in str(message.content).lower(): # Siraj
        if message.author.id == 416430987241586698:
            await message.channel.send("https://media.tenor.co/videos/c8bad30e8d9834c6543b7575c3d7bd89/mp4")
    if "cap" in str(message.content).lower(): # Usmaan
        if message.author.id == 397082457179947029:
            await message.channel.send("yo that's cap'n cap'n")

    # General CaliBot Commands
    if message.content.startswith('/help'): # Help command
        with open("cmds.md") as f:
            cmds = f.read()
        await message.channel.send("__**CaliBot Commands:**__```CSS\n" + cmds + "```")

client.run(token)
##client.logout()
##client.close()
##print("We have logged out of bot client")
