import discord
import random
from discord.ext import commands
from functions.tools import json_write, load_json, Member_Obj
import sys
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix = "£")

bot.remove_command('help')

@bot.event
async def on_ready():
    print("Connected")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="you lose money")) 

@bot.command(name="die")
async def die(ctx):
    if ctx.author.id  == 624654132845740073:
        print("Bye!")
        embed=discord.Embed(title="Oh oh, here we go again!", description="This Bot Is Going Offline!", color=random.randint(0, 16777215))
        await ctx.send(embed=embed)
        sys.exit(0)
    else:
        embed = discord.Embed(description="You are missing the Bot Admin permission required to invoke this command. HAHA SUCKER!!", color=0xff0000)
        await ctx.send(embed=embed)
        

@bot.command(name="help", aliases=["h"])
async def help(ctx, menu=None):
    embed = discord.Embed(title="Pigs Amiright", description="Here are your help commands ig.", color=random.randint(0, 16777215))
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    if menu == "shops":
        embed.add_field(name="Shop Commands", value="`create-shop <colour(base 10 colour code)> <name>|<description>` | Make your shop\n `remove-shop` | Take your shop down \n \
            `add-item <name>|<price>` | add an item to your shop \n `remove-item <item>` | Take an item off your shelves\n `shops` | View the shops\
                 in the server\n `shop <user(optional)>` | look at what someone's shop sells \n `debts` | view the debts people need to pay you \n \
                     `my-debts` | view your outstanding debts ", inline=False)
    elif menu == "orders":
        embed.add_field(name="Order Commands", value="`place-order <shop> <item>|<quantity>` | place an order for some of an item \
                \n `revoke-order <item>` | Cancel an order you have made \n `complete-order <item>` | confirm an incoming order as completed \n \
                `incoming-orders` | View orders people have made for your items \n `outgoing-orders` | View the outstanding orders you have made in other shops ", inline=False)
    elif menu == "auctions":
        embed.add_field(name="Auction Commands", value="`start-auction <name> <item> <quantity(integer)> <starting price(integer)> <year|month|day|hour|minute(the time it ends)(all integers)>` | start an auction \n \
                    `close-auction` | close your existing auction \n `my-auction` | view your open auction (if you have one) \n `auctions` | view all open auctions \n `place-bid <auction> <bid>` | place a bid on an open auction", inline=False)

    else:
        embed.add_field(name="Commands", value="`help <shops, orders, or auctions>` | Displays this message\n `alias-help <shops, orders or auctions>` | shows aliases of commands \n `ping` | Shows the latency of the bot", inline=False)

    embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name="alias-help", aliases=["ah", "alias-h", "al", "You_Can_Call_Me_Al"])
async def alias_help(ctx, menu=None):
    
    embed = discord.Embed(title="Pigs Amiright", description="Here are your aliases ig.", color=random.randint(0, 16777215))
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    if menu == "shops":
        embed.add_field(name="Shop Aliases", value="`create-shop <colour(base 10 colour code)> <name>|<description>` | `cs`, `cre-s`\n `remove-shop` | `rs`, `rem-s`\n \
        `add-item <name>|<price>` | `ai`, `add-i`\n `remove-item <item>` | `ri`, `rem-i`\n `shops` | `ls`, `list-shops`, `stalls`\n \
            `shop <user(optional)>` | `s`, `stall` \n `debts` | `d`, `debt`\n `my-debts` | `md`, `mydebt`", inline=False)
    elif menu == "orders":
        embed.add_field(name="Order Aliases", value="`place-order <shop> <item>|<quantity>` | `po`, `pla-ord`\
            \n `revoke-order <item>` | `ro`, `rev-ord`\n `complete-order <item>` | `co`, `comp-ord`\n `incoming-orders` | `io`, `in-ord`\n \
            `outgoing-orders` | `oo`, `out-ord`", inline=False)
    elif menu == "auctions":
        embed.add_field(name="Auction Aliases", value="`start-auction <name> <item> <quantity(integer)> <starting price(integer)> <year|month|day|hour|minute(the time it ends)(all integers)>` | `st`, `st-auc`\n \
                    `close-auction` | `ca`, `cl-auc`\n `my-auction` | `ma`, `my-auc`\n `auctions` | `a`\n `place-bid <auction> <bid>` | `pb`, `p-bid`", inline=False)
    else:
        embed.add_field(name="Aliases", value="`help` | `h`\n `alias-help` | `ah`, `alias-h`, `al`, `You_Can_Call_Me_Al` \n `ping` | `pong`", inline=False)
    
    embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command(name="ping", aliases=["pong"])
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f'Pong! {round(bot.latency * 1000)}ms', color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

@bot.command(name="PigsPigsPigsPigsPigsPigsPigs", aliases=["PigsPigsPigsPigs", "PigsPigsPigs", "PigsPigs", "Pigs", "Pigsx7"])
async def Pigs(ctx):
    embed = discord.Embed(title="PigsPigsPigsPigsPigsPigsPigs", description="Or Pigs x7, were a rock band formed in Newcastle-upon-Tyne in 2012", color=random.randint(0, 16777215))
    ctx.send(embed=embed)
    
if __name__ == "__main__":
    cogs = ["cogs.shopsCog", "cogs.ordersCog", "cogs.auctionsCog"]
    for cog in cogs:
        bot.load_extension(cog)

while 1:
    t = datetime.now().time()
    if t.second == 0:
        bot.run('ODIzOTI4NzcwMTIwNTE1NjY1.YFn9dg.lCoqMxOwpVnehLnLEjdX1Hsi0rs')
        break
