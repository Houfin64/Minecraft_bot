import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix = "£")

client.remove_command('help')

@client.event
async def on_ready():
  print("Connected")
  await client.change_presence(status=discord.Status.online, activity=discord.Game('£ping'))

@client.command()
async def ping(ctx):
        await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

client.run('ODIzOTI4NzcwMTIwNTE1NjY1.YFn9dg.lCoqMxOwpVnehLnLEjdX1Hsi0rs')
