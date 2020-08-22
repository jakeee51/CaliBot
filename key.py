import os

cwd = os.getcwd()
os.chdir("..");os.chdir("..");os.chdir("..")
os.chdir("Desktop\\Prog\\CaliBot")

def bot_pass():
    with open("bot.txt") as f:
        return f.read()

def db_pass():
    with open("db.txt") as f:
        return f.read()

def email_pass():
    with open("email.txt") as f:
        return f.read()
