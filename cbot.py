import discord
import time
import asyncio

'''
from discord.ext import commands

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('token')
'''

#Learn to edit messages to prevent clutter
#Create exceptions for invalid commands

def timeCheck(t):
    C = False
    if len(t) > 5:
        return False
    elif len(t) == 5:
        if t[:2].isdigit() and t[2] == ':' and t[-2:].isdigit():
            C = True
    elif len(t) == 4:
        if t[0].isdigit() and t[1] == ':' and t[-2:].isdigit():
            C = True
    return C

def timeAdd(hrs, mins):
    newHrs = int(hrs) + 1
    newMin = int(mins) + 30
    if newMin >= 60:
        newHrs += 1
        newMin = newMin - 60
    if newHrs == 13:
        newHrs = '1'
    elif newHrs == 14:
        newHrs = '2'
    if newMin < 10:
        newMin = "0" + str(newMin)
    return str(newHrs) + ':' + str(newMin)

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "/startDFC (Starts Clock)"))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return 0;

    if message.content.startswith('/startDFC'):
        st = message.content
        lst = st.split(' ')
        if len(lst) < 3:
            await message.channel.send("***Invalid Command! Must include start time of server and timezone!***\n (ex: `/startDFC 12:30 EST`)")
            return 0;
        chk = timeCheck(lst[1])
        tz = lst[2]
        if not chk:
            await message.channel.send("***Invalid Command! Must include start time of server and timezone!***\n (ex: `/startDFC 12:30 EST`)")
        else:
            st = lst[1]
            h = st[:2].strip(':')
            m = st[-2:]
            st = timeAdd(h, m)
            await message.channel.send(":pray: Devil Fruit Spawn Time :pray: ```" + st + " " + tz + "```")
            await asyncio.sleep(5400)
            await message.channel.send(message.author.mention + ":open_mouth: The devil fruit has spawned at :open_mouth: :```" + st + " " + tz + "```:triumph:You now have 25 minutes to search!:triumph:")

client.run('NTc2OTUyMjc0MjA3NzY4NTc2.XNd-wA.EubtjmhnTgLnDL6yBBFv4OtojeU')
