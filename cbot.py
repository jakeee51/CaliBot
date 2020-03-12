# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: CaliBot
Functionality Purpose: An agile Discord Bot to fit Cali's needs
Version: 0.1.0
'''
#3/11/20

import discord
import asyncio
import re, os, time, yaml, smtplib
from email.message import EmailMessage
from random import randint
from key import Key, cwd
try:
    import GeoLiberator as GL
except ModuleNotFoundError:
    pass
token = Key()
os.chdir(cwd)

'''
from discord.ext import commands
@bot.command()
async def ping(ctx):
    await ctx.send('pong')
bot.run('token')
'''

#Organize code
#Learn to edit messages to prevent clutter
#Have /verify prompt to specify college

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

def edit_file(file, value):
    with open(file, 'r+') as f:
        lines = f.readlines()
        f.seek(0); found = False
        for line in lines:
            line = line.strip('\n')
            if str(line).lower() != str(value).lower():
                f.write(line + '\n')
            else:
                found = True
        f.truncate()
        return found

def send_email(addr: str) -> str: # Return 4-digit verification code string
    sCode = f"{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}"
    msg = EmailMessage()
    msg.set_content(f"Verification Code Below:\n\n{sCode}")
    msg["Subject"] = "Test 1"
    msg["From"] = "djm65@njit.edu"
    msg["To"] = "jakemorfe@gmail.com"
    s = smtplib.SMTP("localhost")
    s.send_message(msg)
    s.quit()
    return sCode

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "/help (For all cmds)"))
    print("We have logged in as {0.user}".format(client))
    channel = client.get_channel(631090067963772931)
##    await channel.send("`Updated!`")

@client.event
async def on_member_join(member):
    channel = client.get_channel(630888887375364128)
    await channel.send("__***Welcome to the NJIT MSA Discord Server!***__\n\n**Please type `/verify <YOUR_NJIT_UCID>` to join the chat.**")

@client.event
async def on_message(message):
    if message.author == client.user:
        return -1;

    if message.channel.id == 630888887375364128: # Listen on NJIT MSA #verify
        eCode = re.search(r"^\d\d\d\d$", message.content)
        if eCode:
            with open("verify.txt", 'r') as f:
                lines = f.readlines()
                if len(lines) != 0:
                    for line in lines:
                        if line[:4] == eCode.group():
                            await message.channel.send("**Code accepted! Welcome to the NJIT Brotherhood!**")
                            edit_file("verify.txt", line.strip('\n'))
                        else:
                            await message.channel.send("**Invalid code! Who a u?!**")
    if message.content == "my guardian angel":
        if "Cali#6919" == str(message.author):
            await message.channel.send("Dats right, it is I! :stuck_out_tongue:")
    if re.search(r"<@233691753922691072>|CALI", str(message.content)):
        if re.sub(r"<@233691753922691072>", '', str(message.content)).isupper():
            await message.channel.send("***DON'T YELL AT PAPA!!!***")
    
    if message.content.startswith('/help'): # Help command
        await message.channel.send("```CaliBot Commands:\n/help\n/verify\n/GL\n/timer\n```")

    if message.content.startswith('/verify'): # Verify command
        ucid = message.content.strip("/verify ")
        email_addr = f"{ucid}@njit.edu"
        vCode = send_email(email_addr)
        with open("verify.txt", 'a') as f:
            f.write(f"{vCode} {email_addr}\n")
        await message.channel.send(f"**We've sent a verification code to your email at {email_addr}, please copy & paste it below.**")
        await asyncio.sleep(900)
        edit_file("verify.txt", f"{vCode} {email_addr}")

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

client.run(token)
