# -*- coding: utf-8 -*-

from pokebot import *
from tools import *
import re, os, sys, time, json, smtplib, datetime

@bot.event
async def on_reaction_add(reaction, user):
    await reaction.message.channel.send("Test")

@bot.event
async def on_reaction_remove(reaction, user):
    await reaction.message.channel.send("Me")
