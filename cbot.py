# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: CaliBot
Functionality Purpose: An agile Discord Bot to fit Cali's needs
Version: 
'''
RELEASE = "v0.2.9 - 9/18/20"

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
    refresh = []
    with open("refresh.txt") as f: # Delete old role reacts
        lines = f.readlines()
        ch_s = client.get_channel(sisters.role_select)
        ch_b = client.get_channel(brothers.role_select)
        for msg_og in lines:
            role_ch, msg_id = msg_og.split(' ')
            if int(role_ch) == sisters.role_select:
                msg = await ch_s.fetch_message(int(msg_id.strip('\n')))
            else:
                msg = await ch_b.fetch_message(int(msg_id.strip('\n')))
            await msg.delete()
            refresh.append(msg_og.strip('\n'))
    for old_msg in refresh: # Flush role reacts deletions
        edit_file("refresh.txt", old_msg)
    with open("refresh.txt", 'a') as f: # Populate new role reacts
        for CH in CONST_MSG:
            channel = client.get_channel(CH[0])
            for MSG in CH[1]:
                message = await channel.send(MSG.message)
                await message.add_reaction(MSG.reaction)
                f.write(f"{CH[0]} {message.id}\n")

'''@client.event
async def on_member_join(member):
    #await client.edit_message(message_var, "This is the edit to replace the message.")
    channel = client.get_channel(brothers.general)
    await asyncio.sleep(15)
    await channel.send("__***Welcome to the NJIT MSA Discord Server!***__\n\n**Please type `/verify <YOUR_NJIT_UCID>` to join the chat.**")'''

@client.event
async def on_reaction_add(reaction, user):
    if reaction.count == 1 or \
       reaction.message.channel.id != sisters.role_select and \
       reaction.message.channel.id != brothers.role_select:
        return -1
    role_id = listen_role_reaction(reaction.emoji)
    if role_id:
        role = discord.utils.get(
                    client.get_guild(SERVER_ID).roles, id=role_id)
        await user.add_roles(role)

@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id != sisters.role_select and \
       reaction.message.channel.id != brothers.role_select:
        return -1
    role_id = listen_role_reaction(reaction.emoji)
    if role_id:
        role = discord.utils.get(
                    client.get_guild(SERVER_ID).roles, id=role_id)
        await user.remove_roles(role)

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

    if listen_announce(message): # Send to alternate announcement channel
        announce_channel = listen_announce(message)
        channel = client.get_channel(announce_channel)
        await channel.send(message.content)

    if message.content.startswith('/add'): # Add user officially
        if check_admin(message):
            user_id = re.search("\d{5,}", message.content)
            if user_id:
                guild = client.get_guild(SERVER_ID)
                member = guild.get_member(int(user_id.group()))
                sibling, rm_role = get_sibling_role(member)
                role = discord.utils.get(
                    client.get_guild(SERVER_ID).roles, name=f"{sibling}")
                await member.add_roles(role)
                await member.remove_roles(rm_role)
                siblinghood = get_sibling(sibling)
                channel = client.get_channel(siblinghood.general)
                await channel.send("<@!" + user_id.group() + "> *has* ***officially*** *joined the NJIT MSA Discord! Welcome your " + sibling + "!*")
            else:
                await message.channel.send("**Invalid command! Please make sure you're @ing the user.**", delete_after=25)
                await message.delete(delay=300)

    if listen_verify(message): # Verify command
        ucid, gender = listen_verify(message)
        if not re.search(r"^[a-zA-Z]{2,4}\d{0,4}$", ucid) or \
           not re.search(r"(Brother|Sister)", gender) or \
           not re.search(r"^/verify ", str(message.content)):
            await message.channel.send("**Invalid command! Please make sure you're typing everything correctly.**", delete_after=25)
            await message.delete(delay=300)
        else:
            email_addr = f"{ucid}@njit.edu"; ucid = ucid.lower()
            vCode = send_email(email_addr); ID = message.author.id
            with open("verify.txt", 'a') as f:
                f.write(f"{vCode} {email_addr} {ID} {gender}\n")
            temp = await message.channel.send(f"**We've sent a verification code to your email at** ___{email_addr}___**, please copy & paste it below.**", delete_after=300)
            await message.delete(delay=300)
            try:
                await asyncio.wait_for(check_verify(f"{vCode} {email_addr}", message, temp), timeout=900) # Purge messages when record is removed from 'verify.txt' otherwise purge in 15 minutes
            except asyncio.TimeoutError:
                try:
                    await message.delete(); await temp.delete()
                except discord.errors.NotFound:
                    pass
                edit_file("verify.txt", f"{vCode} {email_addr} {ID} {gender}")
    elif listen_code(message): # Listen for 4-digit code on the NJIT MSA #verify
        eCode = listen_code(message)
        if eCode:
            with open("verify.txt") as f:
                lines = f.readlines(); flag = True
                if len(lines) != 0:
                    for line in lines:
                        lst = line.strip('\n').split(' ')
                        if lst[0] == eCode.group() and lst[2] == str(message.author.id): # Verify code
                            edit_file("verify.txt", line.strip('\n'))
                            role = discord.utils.get(client.get_guild(SERVER_ID).roles,
                                                     name=f"{lst[3]}s Waiting Room")
                            await message.author.add_roles(role); flag = False
                            nName = get_name(lst[1])
                            sibling = get_sibling(lst[3])
                            await message.delete()
                            if nName != None:
                                try:
                                    await message.author.edit(nick=f"{nName}")
                                except discord.errors.Forbidden:
                                    print("Success!")
                            channel = client.get_channel(sibling.wait) # NJIT MSA #general
                            await channel.send(f"@here ***" + message.author.mention + "***" + " *has joined the NJIT MSA Discord!*")
                        else:
                            await message.delete(delay=60)
                    if flag:
                        temp = await message.channel.send("**Invalid code! Who a u?!**")
                        await temp.delete(delay=60)
    else: # Delete every other message in #verify in 5 min.
        if message.channel.id == VERIFY_ID:
            await message.delete(delay=300)
    
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

    if message.content.startswith('/showq') and in_general(message.channel.id): # Show queue command
        siblinghood = in_general(message.channel.id) # Return brother or sister server config
        showq = f"{siblinghood.name}_showq.txt"
        if message.content == "/showq":
            with open(showq) as f:
                await message.channel.send(":tickets::popcorn: Shows & Movies Queue List:\n```CSS\n" + f.read() + "```")
        elif message.content.startswith('/showq remove'):
            show = re.sub(r"/showq remove ", '', str(message.content))
            find = edit_file(showq, str(show))
            if find:
                await message.channel.send("`Show or Movie removed from queue!`")
            else:
                await message.channel.send("`Show or Movie not found!`")
        elif message.content.startswith('/showq '):
            show = re.sub(r"/showq ", '', message.content)
            with open(showq, 'r+') as f:
                shows = f.readlines(); exists = False
                for entry in shows:
                    if re.search(fr"{show}", entry.lower()):
                        await message.channel.send("***Sorry, the Show or Movie is already in queue!***")
                        exists = True
                if not exists:
                    f.write(str(show) + '\n')
                    await message.channel.send(":tickets::popcorn:`Show or Movie added to queue!`")

    if message.content.startswith('/GL'): # GeoLiberator demo command
        get = re.sub(r"^/GL ", '', str(message.content))
        result = GL.GeoLiberator(str(get)).getAddress()
        if result == "OTHER":
            result = GL.GeoLiberator(str(get)).full_address()
        await message.channel.send(str(result))

    if message.content.startswith('/herotime'): # It's Ben 10!
	    alien_form = ben_10()
	    await message.channel.send(message.author.mention + f" has transformed into **{alien_form}**!")


    # Sisters Exclusive Commands



    # Brothers Exclusive Commands
    if message.content.startswith('/mods') and message.channel.id == brothers.general: # Manage Minecraft mods command
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
