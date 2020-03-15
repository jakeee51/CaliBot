# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: CaliBot
Functionality Purpose: An agile Discord Bot to fit Cali's needs
Version: 0.1.8
'''
#3/15/20

import discord
import asyncio
import re, os, time, yaml, smtplib
import mysql.connector
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
#Have `/verify` prompt to specify college
#After verified delete all their messages in #verify

#Put more detail into `/help`
#Create a no-reply gmail account
#Prevent email from spam
#syjqqqvdajhssgfl

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
    msg.set_content(f"\
<html><body><b>Your verification code to join the chat is below:<br><br>\
<h2>{sCode}</h2></b>Please copy & paste this code in the \
<i><u>#verify</u></i> text channel of the NJIT MSA Discord. \
This code will expire in 15 minutes.</body></html>", subtype="html")
    msg["Subject"] = "Verification Code for NJIT MSA Discord"
    msg["From"] = "no-reply-njitmsadiscord@njit.edu"
    msg["To"] = addr
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login("djm65@njit.edu", "syjqqqvdajhssgfl")
            s.send_message(msg)
    return sCode

def get_name(addr: str) -> str: # Return full name string based on email
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mantabayray51",
        database="contacts")
    mycursor = mydb.cursor()
    ucid = re.sub(r"@njit\.edu", '', addr)
    sql = f"SELECT full_name FROM links WHERE ucid='{ucid}'"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if len(result) != 0:
        return str(result[0][0])

def check_verify(msg, code):
    end = time.time() + 900 # Time to end function after 15 minutes
    while True:
        if time.time() >= end:
            break
        with open("verify.txt") as f:
            text = f.read()
            if re.search(fr"^{code}", text):
                continue
        break
        
    client.delete_message(msg)

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "/help (For all cmds)"))
    print("We have logged in as {0.user}".format(client))
    channel = client.get_channel(631090067963772931)
    #await channel.send("`Updated!`")

'''@client.event
async def on_member_join(member):
    channel = client.get_channel(630888887375364128)
    await asyncio.sleep(15)
    await channel.send("__***Welcome to the NJIT MSA Discord Server!***__\n\n**Please type `/verify <YOUR_NJIT_UCID>` to join the chat.**")'''

@client.event
async def on_message(message):
    if message.author == client.user:
        return -1;

    if message.channel.id == 688625250832744449: # Listen for code on NJIT MSA #verify
        eCode = re.search(r"^\d\d\d\d$", message.content)
        if eCode:
            with open("verify.txt", 'r') as f:
                lines = f.readlines(); flag = True
                if len(lines) != 0:
                    for line in lines:
                        lst = line.strip('\n').split(' ')
                        if lst[0] == eCode.group() and lst[2] == str(message.author.id): # Verify code
                            edit_file("verify.txt", line.strip('\n'))
                            role = discord.utils.get(client.get_guild(630888887375364126).roles, name="Muslim")
                            await message.author.add_roles(role); flag = False
                            nName = get_name(lst[1])
                            if nName != None:
                                await message.author.edit(nick=f"{nName}")
                                channel = client.get_channel(631090067963772931) # NJIT MSA #general
                                await channel.send(f"***{nName}*** *has joined the NJIT MSA Discord!*")
                    if flag:
                        await message.channel.send("**Invalid code! Who a u?!**")
    if message.content == "nu u":
        if "Cali#6919" == str(message.author):
            await message.channel.send("nu u")
    if re.search(r"<@233691753922691072>|CALI", str(message.content)):
        if re.sub(r"<@233691753922691072>", '', str(message.content)).isupper():
            await message.channel.send("***DON'T YELL AT PAPA!!!***")
    
    if message.content.startswith('/help'): # Help command
        await message.channel.send("```CaliBot Commands:\n/help\n/verify\n/GL\n/timer\n/showq\n/showq remove\n/juegos```")

    if message.content.startswith('/verify'): # Verify command
        ucid = message.content.strip("/verify ")
        email_addr = f"{ucid}@njit.edu"
        vCode = send_email(email_addr)
        with open("verify.txt", 'a') as f:
            f.write(f"{vCode} {email_addr} {message.author.id}\n")
        temp = await message.channel.send(f"**We've sent a verification code to your email at** ___{email_addr}___**, please copy & paste it below.**")
        check_verify(message, vCode) # Purge messages when record is removed from 'verify.txt' otherwise purge in 15 minutes
        client.delete_message(temp)

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
        role = discord.utils.get(client.get_guild(630888887375364126).roles, name="Juegos")
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

client.run(token)
