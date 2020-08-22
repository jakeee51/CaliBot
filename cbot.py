# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: CaliBot
Functionality Purpose: An agile Discord Bot to fit Cali's needs
Version: 0.2.1
'''
#8/22/20

import discord
import asyncio
import re, os, time, yaml, smtplib
from random import randint
from key import bot_pass, cwd
from config import *
from tools import *
try:
    import GeoLiberator as GL
except ModuleNotFoundError:
    pass
token = bot_pass()
os.chdir(cwd)

'''
from discord.ext import commands
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
bot.run('token')
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
import sys
sys.stdout = Unbuffered(sys.stdout)

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "/help (For all cmds)"))
    print("We have logged in as {0.user}".format(client))
    #channel = client.get_channel(brothers.general)
    #await channel.send("`Updated!`")

'''@client.event
async def on_member_join(member):
    #await client.edit_message(message_var, "This is the edit to replace the message.")
    channel = client.get_channel(brothers.general)
    await asyncio.sleep(15)
    await channel.send("__***Welcome to the NJIT MSA Discord Server!***__\n\n**Please type `/verify <YOUR_NJIT_UCID>` to join the chat.**")'''

@client.event
async def on_message(message):
    if message.author == client.user:
        return -1;

    if message.content == "nu u":
        if "Cali#6919" == str(message.author):
            await message.channel.send("nu u")
    
    if message.content.startswith('/help'): # Help command
        with open("cmds.md") as f:
            cmds = f.read()
        await message.channel.send("__**CaliBot Commands:**__```CSS\n" + cmds + "```")
    
    if message.content.startswith('/verify'): # Verify command
        ucid = message.content.strip("/verify ")
        if not re.search(r"^\w{0,4}\d{0,4}$", ucid):
            await message.channel.send("**Invalid command! Please make sure you're typing everything correctly.**", delete_after=30)
        else:
            email_addr = f"{ucid}@njit.edu"
            vCode = send_email(email_addr); ID = message.author.id
            with open("verify.txt", 'a') as f:
                f.write(f"{vCode} {email_addr} {message.author.id}\n")
            temp = await message.channel.send(f"**We've sent a verification code to your email at** ___{email_addr}___**, please copy & paste it below.**", delete_after=900)
            '''try:
                await asyncio.wait_for(check_verify(vCode, message, temp), timeout=900) # Purge messages when record is removed from 'verify.txt' otherwise purge in 15 minutes
            except asyncio.TimeoutError:
                await message.delete(); await temp.delete()
            edit_file("verify.txt", f"{vCode} {email_addr} {ID}")'''

    if message.channel.id == brothers.verify: # Listen for code on NJIT MSA #verify
        eCode = re.search(r"^\d\d\d\d$", message.content)
        if eCode:
            with open("verify.txt") as f:
                lines = f.readlines(); flag = True
                if len(lines) != 0:
                    for line in lines:
                        lst = line.strip('\n').split(' ')
                        if lst[0] == eCode.group() and lst[2] == str(message.author.id): # Verify code
                            edit_file("verify.txt", line.strip('\n'))
                            role = discord.utils.get(client.get_guild(brothers.server).roles, name="Muslim")
                            await message.author.add_roles(role); flag = False
                            nName = get_name(lst[1])
                            if nName != None:
                                await message.author.edit(nick=f"{nName}")
                            channel = client.get_channel(brothers.general) # NJIT MSA #general
                            await channel.send(f"***" + message.author.mention + "***" + " *has joined the NJIT MSA Discord!*")
                            await message.delete()
                        else:
                            await message.delete(delay=60)
                    if flag:
                        temp = await message.channel.send("**Invalid code! Who a u?!**")
                        await temp.delete(delay=60)

    if message.content.startswith('/GL'): # GeoLiberator demo command
        get = re.sub(r"^/GL ", '', str(message.content))
        result = GL.GeoLiberator(str(get)).getAddress()
        await message.channel.send(str(result))

    if message.content.startswith('/timer'): # Set timer command
        t = message.content.strip("/timer ")
        get = re.search(r"^(\d{0,2}) (\d{0,2})$", t)
        if not get:
            await message.channel.send("***Invalid Command! Must include hours followed by minutes!***\n (ex: `/time 0 30`)")
        else:
            eta = ((int(get.group(1)) * 60) * 60) + (int(get.group(2)) * 60)
            await message.channel.send(f"You will be notified in **" + get[1] + "** hour(s) & **" + get[2] + "** minute(s)!")
            await asyncio.sleep(eta)
            await message.channel.send(message.author.mention + " **ALERT! YOUR TIMER HAS RUN OUT! DO WHAT YOU MUST!**")

    if message.content.startswith('/juegos'):
        role = discord.utils.get(client.get_guild(brothers.server).roles, name="Juegos")
        await message.author.add_roles(role)
        await message.channel.send(message.author.mention + " *role has been updated!*")

    if message.content.startswith('/showq'):
        if message.content == "/showq":
            with open("showq.txt") as f:
                await message.channel.send(":tickets::popcorn: Shows & Movies Queue List:\n```CSS\n" + f.read() + "```")
        elif message.content.startswith('/showq remove'):
            show = re.sub(r"/showq remove ", '', str(message.content))
            find = edit_file("showq.txt", str(show))
            if find:
                await message.channel.send("`Show or Movie removed from queue!`")
            else:
                await message.channel.send("`Show or Movie not found!`")
        elif message.content.startswith('/showq '):
            show = re.sub(r"/showq ", '', message.content)
            with open("showq.txt", 'r+') as f:
                shows = f.readlines(); exists = False
                for entry in shows:
                    if re.search(fr"{show}", entry.lower()):
                        await message.channel.send("***Sorry, the Show or Movie is already in queue!***")
                        exists = True
                if not exists:
                    f.write(str(show) + '\n')
                    await message.channel.send(":tickets::popcorn:`Show or Movie added to queue!`")

    if message.content.startswith('/mods'):
        if message.content == "/mods":
            with open("mods.txt") as f:
                await message.channel.send(":video_game::video_game: Minecraft Mods List:\n```CSS\n" + f.read() + "```")
        elif message.content.startswith('/mods remove'):
            mod = re.sub(r"/mods remove ", '', str(message.content))
            find = edit_file("mods.txt", str(mod))
            if find:
                await message.channel.send("`Mod removed from list!`")
            else:
                await message.channel.send("`Mod not found!`")
        elif message.content.startswith('/mods'):
            mod = re.sub(r"/mods ", '', message.content)
            with open("mods.txt", 'r+') as f:
                mods = f.readlines(); exists = False
                for entry in mods:
                    if re.search(fr"{mod}", entry.lower()):
                        await message.channel.send("***The mod is already in list!***")
                        exists = True
                if not exists:
                    f.write(str(mod) + '\n')
                    await message.channel.send(":video_game: `Mod added to list!`")


client.run(token)
##client.logout()
##client.close()
##print("We have logged out of bot client")
