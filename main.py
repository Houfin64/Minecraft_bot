import discord
import random
from discord.ext import commands
from tools import json_write, load_json, Member_Obj

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix = "£")

bot.remove_command('help')

@bot.event
async def on_ready():
  print("Connected")
  await bot.change_presence(status=discord.Status.online, activity=discord.Game('£ping'))

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Pigs amiright", description="here are your help commands ig", color=random.randint(0, 16777215))
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.add_field(name="commands (will update fields later)", value="``help``, ``ping``, ``create-shop``, ``remove-shop`` \n``add-item``, ``remove-item``, ``shops``, ``shop``", inline=False)
    embed.set_footer(text="name is Work-in-progress", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)


@bot.command(name="ping")
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f'Pong! {round(bot.latency * 1000)}ms', color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

@bot.command(name="create-shop")
async def create_shop(ctx, *, argument):

    sdict = await load_json("shops")
    udict = await load_json("users")

    if "|" not in argument:
        embed = discord.Embed(title="Welp, that failed!", description="Syntax: `£create-shop <shop-name> | <description>`", color=0xff0000)
        return await ctx.send(embed=embed)

    name, description = argument.partition("|")[0], argument.partition("|")[2]

    owner = ctx.author.id
    
    if str(owner) in udict:
        embed = discord.Embed(title="Welp that failed!", description="You can't have more than 1 shop, add items instead.  \nIf you want to delete your shop do `£remove-shop` instead, and i will take yor stall down.", color=0xff0000)
        return await ctx.send(embed=embed)
    if name in sdict:
        embed = discord.Embed(title="Welp that failed", description="To avoid errors, please have a unique shop name", color=0xff0000)
        return await ctx.send(embed=embed)

    embed = discord.Embed(title="KK, Thanks", description="I've added you to the shop list :)! do `£add-item` to add items to your shop.", color=0xff0000)
    await ctx.send(embed=embed)

    udict[str(ctx.author.id)] = name
    sdict[name] = {"owner": str(owner), "description": description, "items": {}, "name": name}

    await json_write("shops", sdict)
    await json_write("users", udict)

@bot.command(name="remove-shop")
async def remove_shop(ctx):
    sdict = await load_json("shops")
    udict = await load_json("users")

    if str(ctx.author.id) not in udict:
        embed = discord.Embed(title="You don't have a shop dumbass!", description="Do `£create-shop` to make one :)", color=0xff0000)
        return await ctx.send(embed=embed)

    del sdict[udict[str(ctx.author.id)]]
    del udict[str(ctx.author.id)]
    
    embed = discord.Embed(title="Your stall has been taken down!", color=0x00ff00)
    await ctx.send(embed=embed)

    await json_write("users", udict)
    await json_write("shops", sdict)

@bot.command(name="add-item")
async def add_item(ctx, *, argument):

    if "|" not in argument:
        embed = discord.Embed(title="Welp, that failed!", description="Syntax: `£add-item <item-name> | <price>`", color=0xff0000)
        return await ctx.send(embed=embed)

    item, price = argument.partition("|")[0], argument.partition("|")[2]

    sdict = await load_json("shops")
    udict = await load_json("users")

    try:
        if sdict[udict[str(ctx.author.id)]]["items"][item]:
            embed = discord.Embed(title="Welp, that failed!", description="You already have that item in your shop.  \nDo `£remove-item` if you want to change the price!", color=0xff0000)
            return await ctx.send(embed=embed)
    except KeyError:
        sdict[udict[str(ctx.author.id)]]["items"][item] = price
    sdict[udict[str(ctx.author.id)]]["items"][item] = price

    embed = discord.Embed(title="That's you done :)", description="Your item has been added to your shop", color=0x00ff00)
    await ctx.send(embed=embed)

    await json_write("shops", sdict)

@bot.command(name="remove-item")
async def remove_item(ctx, item):
    sdict = await load_json("shops")
    udict = await load_json("users")

    del sdict[udict[str(ctx.author.id)]]["items"][item]
    
    embed = discord.Embed(title="That's you done :)", description="Your item has been removed from your shop", color=0x00ff00)
    await ctx.send(embed=embed)

    await json_write("shops", sdict)

@bot.command(name="shops")
async def shops(ctx):
    sdict = await load_json("shops")

    embed = discord.Embed(title="Shops", description="These are the shops that people own", color=random.randint(0, 16777215))
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    for elem in sdict:
        embed.add_field(name=elem, value=bot.get_user(int(sdict[elem]["owner"])).name)

    embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

    await json_write("shops", sdict)

@bot.command(name="shop")
async def shop(ctx, *, profiles: Member_Obj = None):
    if profiles == None:
        profiles = [ctx.author]
    if len(profiles) > 1:
        embed = discord.Embed(description="Be more specific for goodness's sake!", color=0xff0000)
        return await ctx.send(embed=embed)
    user = profiles[0]


    sdict = await load_json("shops")
    udict = await load_json("users")

    embed = discord.Embed(title=sdict[udict[str(user.id)]]["name"], description=sdict[udict[str(user.id)]]["description"], color=random.randint(0, 16777215))
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    for elem in sdict[udict[str(user.id)]]["items"]:
        embed.add_field(name=elem, value=sdict[udict[str(user.id)]]["items"][elem])
    embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name="place-order")
async def place_order(ctx, shop, item, quantity):
    pass
    # NOTE:  DM will be sent automatically when order is placed, and a second DM will be sent when revoked to apologise for useless DM

@bot.command(name="revoke-order")
async def revoke_order(ctx, order):
    pass

@bot.command(name="outgoing-orders")
async def my_orders(ctx):
    pass

@bot.command(name="incoming-orders")
async def shop_orders(ctx):
    pass

bot.run('ODIzOTI4NzcwMTIwNTE1NjY1.YFn9dg.lCoqMxOwpVnehLnLEjdX1Hsi0rs')
