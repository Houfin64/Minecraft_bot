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

class Member_Obj(commands.Converter):
    async def convert(self, ctx, arguments):
        profiles = []
        if len(ctx.message.mentions) > 0:
            profiles.append(ctx.guild.get_member(ctx.message.mentions[0].id))
        else:
            try:
                arguments = int(arguments)
                profiles.append(ctx.guild.get_user(arguments))
            except Exception as e:
                for member in ctx.guild.members:
                    if str(arguments).lower() in ("{}#{}".format(member.name, member.discriminator)).lower() or str(arguments).lower() in (member.display_name).lower():
                        profiles.append(member)
        return profiles