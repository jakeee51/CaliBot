import os

cwd = os.getcwd()
os.chdir("..");os.chdir("..");os.chdir("..")
os.chdir("Desktop\\Prog\\CaliBot")

def Key():
    with open("key.txt") as f:
        return f.read()
