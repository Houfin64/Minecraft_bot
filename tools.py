import discord
import random
import json
from discord.ext import commands

async def load_json(file):
    with open("./{}.json".format(file), "r") as fj:
        fdict = json.load(fj)
    return fdict

async def json_write(file, dict):
    with open("./{}.json".format(file), "w") as fj:
        json.dump(dict, fj)