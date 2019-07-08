import os

os.chdir("..");os.chdir("..");os.chdir("..")
os.chdir("Desktop\\Python Prog\\CaliBot")
cwd = str(os.getcwd())

def Key():
    with open("key.txt") as f:
        return f.read()
