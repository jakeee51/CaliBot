import discord
import time
import asyncio
import re

'''
from discord.ext import commands

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('token')
'''

#Learn to edit messages to prevent clutter
#Permissions to only work in specific channel

def timeCheck(t):
    C = False
    if len(t) > 5:
        return False
    elif len(t) == 5:
        if t[:2].isdigit() and t[2] == ':' and t[-2:].isdigit() and int(t[:2]) < 24 and int(t[-2:]) < 60:
            C = True
    elif len(t) == 4:
        if t[0].isdigit() and t[1] == ':' and t[-2:].isdigit() and int(t[-2:]) < 60:
            C = True
    return C

def timeAdd(hrs, mins):
    newHrs = int(hrs) + 1
    newMin = int(mins) + 30
    if newMin >= 60:
        newHrs += 1
        newMin = newMin - 60
    if int(hrs) > 12:
        if newHrs == 24:
            newHrs = '00'
        elif newHrs == 25:
            newHrs = '01'
        if newMin < 10:
            newMin = '0' + str(newMin)
    else:
        if newHrs == 13:
            newHrs = '1'
        elif newHrs == 14:
            newHrs = '2'
        if newMin < 10:
            newMin = '0' + str(newMin)
    return str(newHrs) + ':' + str(newMin)

def timeDif(t1, t2): #df spawn time, current time
    if t1 == t2:
        return 1;
    h1 = int(t1[:2].strip(':'))
    h2 = int(t2[:2].strip(':'))
    m1 = int(t1[-2:])
    m2 = int(t2[-2:])
    if h1 > h2:
        hd = h1 - h2
    else:
        hd = h2 - h1
    if m1 > m2:
        md = m1 - m2
    else:
        if h1 != h2:
            return 7117;
        md = m2 - m1
    return (((hd * 60) + md) * 60);

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "/help (For all cmds)"))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return -1;

    if message.content.startswith('/hugPrescription'):
        if "Vampy#1379" in str(message.author) or "Cali#6919" in str(message.author):
            await message.channel.send("***I'm prescribing you 2 hugs per day...Doctor's orders.*** " + message.author.mention)
            await asyncio.sleep(2)
            while True:
                await message.channel.send("https://cdn.discordapp.com/attachments/571528488809660476/586733560388386841/image0.gif")
                await asyncio.sleep(43200)
                await message.channel.send("https://cdn.discordapp.com/attachments/571528488809660476/586733569817182208/image0.gif")
                await asyncio.sleep(43200)

    if message.content.startswith('/help'):
        await message.channel.send("```CaliBot Commands:\n/lick\n/jump\n/assault\n/startDFC```")
    if message.content == "my guardian angel":
        if "Cali#6919" in str(message.author):
            await message.channel.send("That's right papa :P")
    if re.search(r"(punch|slap|bully|insult|kill)", str(message.content)):
        usr = message.content
        get = re.search(r"<@\d+>", usr)
        if '<@233691753922691072>' == get[0]:
            await message.channel.send("Your assault has been deflected! " + message.author.mention)
    if message.content.startswith('/assault'):
        usr = message.content
        usr = usr.strip('/assault ')
        await message.channel.send(message.author.mention + " HAS BEGUN A FULL")
        await asyncio.sleep(2)
        await message.channel.send("SCALE")
        await asyncio.sleep(2)
        await message.channel.send("ATTACK!!!")
        await asyncio.sleep(2)
        await message.channel.send("+slap " + usr)
        await message.channel.send("owo slap " + usr)
        await message.channel.send("->slap " + usr)
    if message.content.startswith('/lick'):
        usr = message.content
        usr = usr.strip('/lick ')
        await message.channel.send(message.author.mention + " *GAVE A* ***MOIST*** *LICK TO* " + usr)
    if message.content.startswith('/jump'):
        await message.channel.send("How high?!" + message.author.mention)
    if message.content.startswith('/startDFC'):
##        ct = time.strftime("%I:%M %c", message.created_at)
##        print(time.time())
##        print(message.created_at) #2019-05-14 06:30:37.141000
##        print(time.strftime("%Y-%m-%d %H:%M:%S %c", time.localtime(time.time())))
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
            dt = timeAdd(h, m)
            await message.channel.send(":pray: Devil Fruit Spawn Time :pray: ```" + dt + " " + tz + "```")
##            sec = timeDif(dt, ct)
##            await message.channel.send("df->" + dt + "ct->" + ct)
##            if sec <= 5400:
##                await asyncio.sleep(sec)
##                await message.channel.send(message.author.mention + ":open_mouth: The devil fruit has spawned at :open_mouth: ```" + dt + " " + tz + "```:triumph:You now have 25 minutes to search!:triumph:")

client.run('NTc2OTUyMjc0MjA3NzY4NTc2.XNd-wA.EubtjmhnTgLnDL6yBBFv4OtojeU')
