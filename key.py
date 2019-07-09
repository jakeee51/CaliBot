import os

cwd = os.getcwd()
os.chdir("..");os.chdir("..");os.chdir("..")
os.chdir("Desktop\\Python Prog\\CaliBot")

def Key():
    with open("key.txt") as f:
        return f.read()
