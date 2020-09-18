import asyncio
import re, os, time, yaml, smtplib
import mysql.connector
from random import randint
from email.message import EmailMessage
from key import db_pass, email_pass
from config import *
login = db_pass()
app_pass = email_pass()

#If email treated as spam:
 #https://support.google.com/mail/contact/bulk_send_new?rd=1

BEN_10 = ["Heatblast", "Wildmutt", "Diamondhead", "XLR8", "Grey Matter",
          "Four Arms", "Stinkfly", "Ripjaws", "Upgrade", "Ghostfreak",
          "Cannonbolt", "Ditto", "Way Big", "Way Thick", "Upchuck",
          "Wildvine", "Alien X", "Echo Echo", "Brainstorm", "Swampfire",
          "Humongousaur", "Jetray", "Big Chill", "Chromastone", "Goop",
          "Spidermonkey", "Rath", "Nanomech"]

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

def send_email(addr: str, test=False) -> str: # Return 4-digit verification code string
    sCode = f"{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}"
    if not test:
        msg = EmailMessage()
        msg.set_content(f"\
    <html><body><b>Your verification code to join the chat is below:<br><br>\
    <h2>{sCode}</h2></b>Please copy & paste this code in the \
    <i><u>#verify</u></i> text channel of your NJIT MSA Discord. \
    This code will expire in 15 minutes.</body></html>", subtype="html")
        msg["Subject"] = "Verification Code for NJIT MSA Discord"
        msg["From"] = "noreply.njitmsa.discord@gmail.com"
        msg["To"] = addr
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login("noreply.njitmsa@gmail.com", app_pass)
                s.send_message(msg)
    else:
        print(sCode)
    return sCode

def get_name(addr: str) -> str: # Return full name string based on email
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=login,
            database="contacts")
        mycursor = mydb.cursor()
        ucid = re.sub(r"@njit\.edu", '', addr)
        sql = f"SELECT full_name FROM links WHERE ucid='{ucid}'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        if len(result) != 0:
            return str(result[0][0])
    except mysql.connector.Error as err:
        print(f"Error: Could not connect:\n\tDetails: {err}")

def check_admin(msg):
    roles = msg.author.roles
    for role in roles:
        if role.name == "Admin" or role.name == "Shura":
            return True
    return False

def ben_10(choice=''):
    choice = choice.strip(' ')
    if choice == '':
        idx = randint(0,28)
        alien_form = BEN_10[idx]
    else:
    	for alien in BEN_10:
	        if alien.lower() in choice.lower():
	            got = randint(1,3)
	            if got == 1:
	                alien_form = alien
	            else:
	                ignore = BEN_10.index(alien)
	                idx = randint(0,27)
	                temp = BEN_10[:ignore] + BEN_10[ignore+1:]
	                alien_form = temp[idx]
    return alien_form

def get_sibling_role(member):
    roles = member.roles; ret = None
    for role in roles:
        if role.name == "Brothers Waiting Room":
            ret = ("Brother", role); break
        elif role.name == "Sisters Waiting Room":
            ret = ("Sister", role); break
    return ret

def get_sibling(sibling):
    if sibling == "Brother":
        return brothers
    else:
        return sisters

def listen_announce(msg):
    if msg.channel.id == brothers.announce:
        if "@everyone" in msg.content:
            return sisters.announce
    elif msg.channel.id == sisters.announce:
        if "@everyone" in msg.content:
            return brothers.announce
    else:
        False

def listen_role_reaction(emoji):
    role_id = 0
    if emoji == "\U0001f9d5": # Mentee
        role_id = 750931950964965506
    elif emoji == "\N{BABY}": # Freshies
        role_id = 750922989972750337
    elif emoji == "\N{GIRL}": # Sophs
        role_id = 750923173956026438
    elif emoji == "\N{WOMAN}": # Juniors
        role_id = 750923497101983795
    elif emoji == "\N{OLDER WOMAN}": # Seniors
        role_id = 750923619634249740
    elif emoji == "\N{STRAIGHT RULER}": # MATH
        role_id = 756328774764593173
    elif emoji == "\N{DESKTOP COMPUTER}": # CS
        role_id = 756329639588397197
    elif emoji == "\N{ATOM SYMBOL}": # PHYS
        role_id = 756334778881540137
    elif emoji == "\N{TEST TUBE}": # CHEM
        role_id = 756335021933068288
    else:
        return False
    return role_id

def listen_verify(msg):
    if msg.channel.id == VERIFY_ID:
        if msg.content.startswith('/verify'):
            request = re.sub(r"/verify ", '', msg.content)
            gender = re.search(r"(brothers?|sis(tas?|ters?))", request) or ''
            if gender:
                ucid = re.sub(fr"{gender.group()}", '', request).strip(' ')
                if gender.group()[0] == 'b':
                    gender = "Brother"
                else:
                    gender = "Sister"
                return ucid, gender
            return ('', '')

def listen_code(msg):
    if msg.channel.id == VERIFY_ID:
        return re.search(r"^\d\d\d\d$", msg.content)

def in_general(channel_id):
    if channel_id == brothers.general:
        return brothers
    elif channel_id == sisters.general:
        return sisters
    else:
        return False

async def check_verify(record, msg, temp):
    while True:
        with open("verify.txt") as f:
            text = f.read()
            if not re.search(fr"{record}", text):
                break
        await asyncio.sleep(0)
    await msg.delete(); await temp.delete()
