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

def listen_verify(channel_id):
    if channel_id == brothers.verify:
        return brothers
    elif channel_id == sisters.verify:
        return sisters
    else:
        return False

def in_general(channel_id):
    if channel_id == brothers.general:
        return brothers
    elif channel_id == sisters.general:
        return sisters
    else:
        return False

'''async def check_verify(record, msg, temp):
    while True:
        with open("verify.txt") as f:
            text = f.read()
            if not re.search(fr"{record}", text):
                break
        await asyncio.sleep(0)
    await msg.delete(); await temp.delete()'''
