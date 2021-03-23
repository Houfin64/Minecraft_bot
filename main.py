import discord
import random
from discord.ext import commands
from shop import Shop

client = commands.Bot(command_prefix = "£")

client.remove_command('help')

@client.event
async def on_ready():
  print("Connected")
  await client.change_presence(status=discord.Status.online, activity=discord.Game('£ping'))

@client.command(name="ping")
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f'Pong! {round(client.latency * 1000)}ms', color=random.randint(0, 16777216))
    await ctx.send(embed=embed)

@client.command(name="create-shop")
async def create_shop(ctx):
    embed = discord.Embed(title="Welcome to the Shop interface!", description="Please tell me the name of your shop!", color=random.randint(0, 16777216))
    await ctx.send(embed=embed)

    message = await client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    content = message.content
    name = content
    owner = message.author.id
    embed = discord.Embed(title="Welcome to the Shop interface!", description="Please give me a description of your shop!", color=random.randint(0, 16777216))
    await ctx.send(embed=embed)

    message = await client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    content = message.content
    description = content
    embed = discord.Embed(title="Welcome to the Shop interface!", description="Please tell me what you will sell!", color=random.randint(0, 16777216))
    await ctx.send(embed=embed)

    message = await client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    content = content
    items = message.content

    shop = Shop(name, description, owner, items)

    print(shop.items)

client.run('ODIzOTI4NzcwMTIwNTE1NjY1.YFn9dg.lCoqMxOwpVnehLnLEjdX1Hsi0rs')
