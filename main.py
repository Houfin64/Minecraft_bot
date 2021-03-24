import discord
import random
from discord.ext import commands
from shop import Shop
from tools import json_write, load_json

client = commands.Bot(command_prefix = "£")

client.remove_command('help')

@client.event
async def on_ready():
  print("Connected")
  await client.change_presence(status=discord.Status.online, activity=discord.Game('£ping'))

@client.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Pigs amiright", description="here are your help commands ig")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.add_field(name="commands (will update fields later)", value="``create_shop``, ``ping``", inline=False)
    embed.set_footer(text="name is Work-in-progress", icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)


@client.command(name="ping")
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f'Pong! {round(client.latency * 1000)}ms', color=random.randint(0, 16777216))
    await ctx.send(embed=embed)

@client.command(name="create-shop")
async def create_shop(ctx):

    sdict = await load_json("shops")
    udict = await load_json("users")

    embed = discord.Embed(title="Welcome to the Shop interface!", description="Please tell me the name of your shop!", color=random.randint(0, 16777216))
    await ctx.send(embed=embed)

    message = await client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    content = message.content
    name = content
    owner = ctx.author.id
    if str(owner) in udict:
        embed = discord.Embed(title="Welp that failed!", description="You can't have more than 1 shop, add items instead.  \nIf you want to delete your shop do `£remove-shop` instead, and i will take yor stall down.", color=random.randint(0, 16777216))
        return await ctx.send(embed=embed)
    if name in sdict:
        embed = discord.Embed(title="Welp that failed", description="To avoid errors, please have a unique shop name", color=random.randint(0, 16777216))
        return await ctx.send(embed=embed)

    embed = discord.Embed(title="Welcome to the Shop interface!", description="Please give me a description of your shop!", color=random.randint(0, 16777216))
    await ctx.send(embed=embed)

    message = await client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    content = message.content
    description = content
    embed = discord.Embed(title="Welcome to the Shop interface!", description="Please tell me what you will sell! (format: `<item>: [price]`)", color=random.randint(0, 16777216))
    await ctx.send(embed=embed)

    message = await client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    content = content
    items = message.content
    embed = discord.Embed(title="KK, Thanks", description="I've added you to the shop list :)!", color=random.randint(0, 16777216))
    await ctx.send(embed=embed)

    udict[str(ctx.author.id)] = name
    sdict[name] = {"owner": str(owner), "description": description, "items": items}

    await json_write("shops", sdict)
    await json_write("users", udict)

@client.command(name="remove-shop")
async def remove_shop(ctx):
    sdict = await load_json("shops")
    udict = await load_json("users")

    if str(ctx.author.id) not in udict:
        embed = discord.Embed(title="You don't have a shop dumbass!", description="Do `£create-shop` to make one :)", color=random.randint(0, 16777216))
        return await ctx.send(embed=embed)

    del sdict[udict[str(ctx.author.id)]]
    del udict[str(ctx.author.id)]
    
    embed = discord.Embed(title="Your stall has been taken down!", color=random.randint(0, 16777216))
    await ctx.send(embed=embed)

    await json_write("users", udict)
    await json_write("shops", sdict)

client.run('ODIzOTI4NzcwMTIwNTE1NjY1.YFn9dg.lCoqMxOwpVnehLnLEjdX1Hsi0rs')
