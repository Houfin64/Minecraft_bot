import discord
import random
from discord.ext import commands
from tools import json_write, load_json

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix = "£")

bot.remove_command('help')

@bot.event
async def on_ready():
  print("Connected")
  await bot.change_presence(status=discord.Status.online, activity=discord.Game('£ping'))

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Pigs amiright", description="here are your help commands ig", color=16777215)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.add_field(name="commands (will update fields later)", value="``create-shop``, ``ping``", inline=False)
    embed.set_footer(text="name is Work-in-progress", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)


@bot.command(name="ping")
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f'Pong! {round(bot.latency * 1000)}ms', color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

@bot.command(name="create-shop")
async def create_shop(ctx):

    sdict = await load_json("shops")
    udict = await load_json("users")

    embed = discord.Embed(title="Welcome to the Shop interface!", description="Please tell me the name of your shop!", color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

    message = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    content = message.content
    name = content
    owner = ctx.author.id
    if str(owner) in udict:
        embed = discord.Embed(title="Welp that failed!", description="You can't have more than 1 shop, add items instead.  \nIf you want to delete your shop do `£remove-shop` instead, and i will take yor stall down.", color=random.randint(0, 16777216))
        return await ctx.send(embed=embed)
    if name in sdict:
        embed = discord.Embed(title="Welp that failed", description="To avoid errors, please have a unique shop name", color=random.randint(0, 16777215))
        return await ctx.send(embed=embed)

    embed = discord.Embed(title="Welcome to the Shop interface!", description="Please give me a description of your shop!", color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

    message = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    content = message.content
    description = content
    embed = discord.Embed(title="KK, Thanks", description="I've added you to the shop list :)! do `£add-item` to add items to your shop.", color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

    udict[str(ctx.author.id)] = name
    sdict[name] = {"owner": str(owner), "description": description, "items": {}}

    await json_write("shops", sdict)
    await json_write("users", udict)

@bot.command(name="remove-shop")
async def remove_shop(ctx):
    sdict = await load_json("shops")
    udict = await load_json("users")

    if str(ctx.author.id) not in udict:
        embed = discord.Embed(title="You don't have a shop dumbass!", description="Do `£create-shop` to make one :)", color=random.randint(0, 16777215))
        return await ctx.send(embed=embed)

    del sdict[udict[str(ctx.author.id)]]
    del udict[str(ctx.author.id)]
    
    embed = discord.Embed(title="Your stall has been taken down!", color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

    await json_write("users", udict)
    await json_write("shops", sdict)

@bot.command(name="add-item")
async def add_item(ctx):
    sdict = await load_json("shops")
    udict = await load_json("users")

    embed = discord.Embed(title="Welcome to the Shop interface!", description="Please tell me the name of the item you are selling!", color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

    message = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    item = message.content

    embed = discord.Embed(title="Welcome to the Shop interface!", description="How much are you selling them for?", color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

    message = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    price = message.content

    sdict[udict[str(ctx.author.id)]]["items"][item] = price
    
    embed = discord.Embed(title="That's you done :)", description="Your item has been added to your shop", color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

    await json_write("shops", sdict)

@bot.command(name="remove-item")
async def remove_item(ctx):
    sdict = await load_json("shops")
    udict = await load_json("users")

    embed = discord.Embed(title="Welcome to the Shop interface!", description="Please tell me the name of the item you are removing!", color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

    message = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    item = message.content

    del sdict[udict[str(ctx.author.id)]]["items"][item]
    
    embed = discord.Embed(title="That's you done :)", description="Your item has been removed from your shop", color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

    await json_write("shops", sdict)

@bot.command(name="shops")
async def shops(ctx):
    sdict = await load_json("shops")

    embed = discord.Embed(title="Shops", description="These are the shops that people own", color=random.randint(0, 16777215))
    for elem in sdict:
        embed.add_field(name=elem, value=bot.get_user(int(sdict[elem]["owner"])).name)
    await ctx.send(embed=embed)

    await json_write("shops", sdict)

@bot.command(name="shop")
async def shops(ctx, user):
    sdict = await load_json("shops")

    embed = discord.Embed(title="Shops", description="These are the shops that people own", color=random.randint(0, 16777215))
    for elem in sdict:
        embed.add_field(name=elem, value=bot.get_user(int(sdict[elem]["owner"])).name)
    await ctx.send(embed=embed)

    await json_write("shops", sdict)

bot.run('ODIzOTI4NzcwMTIwNTE1NjY1.YFn9dg.lCoqMxOwpVnehLnLEjdX1Hsi0rs')
