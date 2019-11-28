import discord
import time
import asyncio
import re
import random
import yaml
import os
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
#Quote guessing game
#Learn to edit messages to prevent clutter
#Permissions to only work in specific channel

pokemonDict = ["Pikachu", "Squirtle", "Charmander", "Bulbasaur"]

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

def getIncrParse(text, idx, pas, last):
    if idx == last:
        part = text[0:2000*last]
        get = re.sub(r"```", '', part)
        get = re.search(r"(.*\n)+", get)
        new_text = re.sub(r"```", '', text)
        part2 = new_text[len(get.group()):]
        return part2
    else:
        part = text[2000*idx:2000*pas]
        get = re.sub(r"```", '', part)
        get = re.search(r"(.*\n)+", get)
    if get:
        return get.group()

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

def timeCheck(t): #check if time is valid
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

def timeAdd(hrs, mins): #add time df takes to spawn
    newHrs = int(hrs) + 1 #add 1 hour
    newMin = int(mins)
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
    channel = client.get_channel(577547595170185217); i = 0
    await channel.send("`Updated!`")
    '''while True:
        spawn = random.choice(pokemonDict)
        if spawn != '':
            with open("play.txt", 'a') as f:
                f.write(f"{i}\t{spawn}\n")
            i += 1
            print(f"{i}\t{spawn}")
            await channel.send("Attention nearby pokemon trainers who are online...! A ***" + spawn + "*** has spawned! Gotta catchem all!\nCapture with `/capture <pokemon_name>`")
        await asyncio.sleep(1200)'''

    '''await channel.send("***I'm prescribing you 3 hugs per day...Doctor's orders.*** *(Note: DO NOT OVERDOSE)* ")
    await asyncio.sleep(2)
    while True:
        await channel.send("<@508740700213477386>" + " https://cdn.discordapp.com/attachments/571528488809660476/586733560388386841/image0.gif")
        await asyncio.sleep(28800)
        await channel.send("<@508740700213477386>" + " https://cdn.discordapp.com/attachments/571528488809660476/586733569817182208/image0.gif")
        await asyncio.sleep(28800)'''

@client.event
async def on_message(message):
    if message.author == client.user:
        return -1;

    if message.content == "my guardian angel":
        if "Cali#6919" == str(message.author) or "Vampy#1379" == str(message.author) or "Sauce Boss#7075" == str(message.author):
            await message.channel.send("That's right, it is I! :stuck_out_tongue:")
    if re.search(r"(<@233691753922691072>|cali)|(<@!508740700213477386>|vampy)|(<@!375778063356657666>|sauce|saucy)", str(message.content).lower()):
        if re.search(r"(punch|slap|bully|insult|kill|baka|roast|trigger|meme|mock|fight|hack|lick)", str(message.content).lower()):
            await message.channel.send("Your assault has been deflected! " + message.author.mention)
            await asyncio.sleep(2)
            await message.channel.send("***Better luck next time!*** :shrug:")
    if re.search(r"<@233691753922691072>|CALI", str(message.content)):
        if re.sub(r"<@233691753922691072>", '', str(message.content)).isupper():
            await message.channel.send("***DON'T YELL AT PAPA!!!***")
#/help
    if message.content.startswith('/help'):
        await message.channel.send("```CaliBot Commands:\n/help\n/GL\n/hit\n/startDFC\n/timer\n/showq\n/showq remove\n/cartoonQs\n/cartoonQs remove\n/vibes\n/vibes remove\n/getPokemon (W.I.P.)```")

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
            show = message.content.strip("/showq ")
            with open("showq.txt", 'r+') as f:
                shows = f.readlines(); exists = False
                for entry in shows:
                    if re.search(fr"{show}", entry):
                        await message.channel.send("***Sorry, the Show or Movie is already in queue!***")
                        exists = True
                if not exists:
                    f.write(str(show) + '\n')
                    await message.channel.send(":tickets::popcorn:`Show or Movie added to queue!`")

    if message.content.startswith('/GL'):
        get = re.sub(r"^/GL ", '', str(message.content))
        result = GL.GeoLiberator(str(get)).getAddress()
        await message.channel.send(str(result))

    if message.content.startswith('/start game'):
        game = message.content.strip("/start game ")
        if game.lower() == "pokemon":
            with open("server_channels.txt", 'a') as f:
                f.write(str(message.channel.id) + '\n')
            await message.channel.send("***Pokemon game has begun!!! Prepare yourselves young trainers!***")
    if message.content.startswith('/stop game'):
        game = re.sub(r"^/stop game ", '', message.content)
        if game.lower() == "pokemon":
            edit_file("server_channels.txt", message.channel.id)
            await message.channel.send("***Pokemon game has been stopped!***")
    if message.content.startswith('/capture'):
        pass #Remove specified pokemon from play.yaml and into player_data.yaml

    if message.content.startswith('/cartoonQs'):
        if message.content == "/cartoonQs":
            with open("cartoonQs.txt") as f:
                lines = f.readlines()
                if len(lines) != 0:
                    cQ = lines[random.randint(0,len(lines)-1)]
                    await message.channel.send("Here's some good cartoonQs from ```CSS\n" + cQ)
                else:
                    await message.channel.send("***Cartoon quote container is empty! Fill it up with:***\n`/cartoonQs <Quote_Vibe>`")
        elif message.content == "/cartoonQs list":
            if "Cali#6919" == str(message.author) or "Vampy#1379" == str(message.author) or "Sauce Boss#7075" == str(message.author):
                with open("cartoonQs.txt") as f:
                    c = f.read(); cnt = len(c)
                    if cnt > 2000:
                        multi = (cnt // 2000)
                        for i in range(multi+1):
                            cartoonQs = getIncrParse(c, i, i+1, multi)
                            await message.channel.send("```CSS\n" + cartoonQs + "```")
                    else:
                        cartoonQs = re.sub(r"```", '', c)
                        await message.channel.send("```CSS\n" + cartoonQs + "```")
        elif message.content.startswith("/cartoonQs remove"):
            get = re.sub("^/cartoonQs remove ", '', str(message.content)) + "```"
            find = edit_file("cartoonQs.txt", str(get))
            if find:
                await message.channel.send("`Cartoon quote removed!`")
            else:
                await message.channel.send("`Cartoon quote not found!`")
        else:
            get = re.sub("^/cartoonQs ", '', str(message.content))
            with open("cartoonQs.txt", 'a') as f:
                f.write(str(message.author) + ": " + re.sub(r":", '', str(get)) + '```\n')
                await message.channel.send("`Cartoon quote added! Thanks!`")
    if re.search(r"^/vibes", str(message.content.lower())):
        if message.content.lower() == "/vibes":
            with open("vibes.txt") as f:
                lines = f.readlines()
                if len(lines) != 0:
                    vibe = lines[random.randint(0,len(lines)-1)]
                    await message.channel.send("Here's some good vibes from ```CSS\n" + vibe)
                else:
                    await message.channel.send("***Vibe container is empty! Fill it up with:***\n`/vibes <Quote_Vibe>`")
        elif message.content.startswith('/vibes list'):
            if "Cali#6919" == str(message.author) or "Vampy#1379" == str(message.author):
                with open("vibes.txt") as f:
                    v = f.read(); cnt = len(v)
                    if cnt > 2000:
                        multi = (cnt // 2000)
                        for i in range(multi+1):
                            vibes = getIncrParse(v, i, i+1, multi)
                            await message.channel.send("```CSS\n" + vibes + "```")
                    else:
                        vibes = re.sub(r"```", '', v)
                        await message.channel.send("```CSS\n" + vibes + "```")
        elif message.content.startswith("/vibes remove"):
            get = re.sub("^/vibes remove ", '', str(message.content)) + "```"
            find = edit_file("vibes.txt", str(get))
            if find:
                await message.channel.send("`Vibe removed!`")
            else:
                await message.channel.send("`Vibe not found!`")
        else:
            get = re.sub("^/vibes ", '', str(message.content))
            with open("vibes.txt", 'a') as f:
                f.write(str(message.author) + ": " + re.sub(r":", '', str(get)) + '```\n')
                await message.channel.send("`Vibe added! Thanks!`")

    if message.content.startswith('/timer'):
        t = message.content.strip("/timer ")
        get = re.search(r"^(\d{0,2}) (\d{0,2})$", t)
        if not get:
            await message.channel.send("***Invalid Command! Must include hours followed by minutes!***\n (ex: `/time 0 30`)")
        else:
            eta = ((int(get.group(1)) * 60) * 60) + (int(get.group(2)) * 60)
            await message.channel.send(f"You will be notified in **" + get[1] + "** hour(s) & **" + get[2] + "** minute(s)!")
            await asyncio.sleep(eta)
            await message.channel.send(message.author.mention + " **ALERT! YOUR TIMER HAS RUN OUT! DO WHAT YOU MUST!**")

    if message.content.startswith('/hit'):
        if "<@233691753922691072>" in str(message.content):
            await message.channel.send("Sorry...I don't hit my papa.")
            await asyncio.sleep(2)
            await message.channel.send("YOU FOO!!!")
        else:
            usr = re.search(r"<@!?\d+>", str(message.content))
            print(str(message.content))
            await message.channel.send(message.author.mention + " ***ATTACKED*** " + usr[0] + " https://tenor.com/view/shizuo-durarara-drrr-gif-12251387")

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
            dt = timeAdd(h, m)
            await message.channel.send(":pray: Devil Fruit Spawn Time :pray: ```" + dt + " " + tz + "```")

client.run(token)
