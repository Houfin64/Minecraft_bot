import discord
import random
from discord.ext import commands
from functions.tools import json_write, load_json, Member_Obj

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix = "£")

bot.remove_command('help')

@bot.event
async def on_ready():
    print("Connected")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('£ping'))

@bot.command(name="help", aliases=["h"])
async def help(ctx):
    embed = discord.Embed(title="Pigs Amiright", description="Here are your help commands ig.", color=random.randint(0, 16777215))
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.add_field(name="Commands", value="``help`` | Displays this message\n ``alias-help`` | shows aliases of commands \n ``ping`` | Shows the latency of the bot\n ``create-shop <name>|<description>`` | Make your shop\n ``remove-shop`` | Take your shop down \n \
        ``add-item <name>|<price>`` | add an item to your shop \n ``remove-item <item>`` | Take an item off your shelves\n ``shops`` | View the shops in the server\n ``shop <user(optional)>`` | look at what someone's shop sells \n ``place-order <shop> <item>|<quantity>`` | place an order for some of an item \
            \n ``revoke-order <item>`` | Cancel an order you have made \n ``complete-order <item>`` | confirm an incoming order as completed \n ``incoming-orders`` | View orders people have made for your items \n \
            ``outgoing-orders`` | View the outstanding orders you have made in other shops \n ``debts`` | view the debts people need to pay you \n ``my-debts`` | view your outstanding debts", inline=False)
    embed.set_footer(text="PigsPigsPigsPigs", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name="alias-help", aliases=["ah", "alias-h", "al", "You_Can_Call_Me_Al"])
async def alias_help(ctx):
    embed = discord.Embed(title="Pigs Smiright", description="Here are your aliases ig.", color=random.randint(0, 16777215))
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.add_field(name="commands (will update fields later)", value="``help`` | ``h``\n ``alias-help`` | ``ah``, ``alias-h``, ``al``, ``You_Can_Call_Me_Al`` \n ``ping`` | ``pong``\n ``create-shop <name>|<description>`` | ``cs``, ``cre-s``\n ``remove-shop`` | ``rs``, ``rem-s``\n \
        ``add-item <name>|<price>`` | ``ai``, ``add-i``\n ``remove-item <item>`` | ``ri``, ``rem-i``\n ``shops`` | ``ls``, ``list-shops``, ``stalls``\n ``shop <user(optional)>`` | ``s``, ``stall``\n ``place-order <shop> <item>|<quantity>`` | ``po``, ``pla-ord``\
            \n ``revoke-order <item>`` | ``ro``, ``rev-ord``\n ``complete-order <item>`` | ``co``, ``comp-ord``\n ``incoming-orders`` | ``io``, ``in-ord``\n \
            ``outgoing-orders`` | ``oo``, ``out-ord``\n ``debts`` | ``d``, ``debt``\n ``my-debts`` | ``md``, ``mydebt``", inline=False)
    embed.set_footer(text="PigsPigsPigsPigs", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)


@bot.command(name="ping", aliases=["pong"])
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f'Pong! {round(bot.latency * 1000)}ms', color=random.randint(0, 16777215))
    await ctx.send(embed=embed)

if __name__ == "__main__":
    cogs = ["cogs.shopsCog", "cogs.ordersCog"]
    for cog in cogs:
        bot.load_extension(cog)

bot.run('ODIzOTI4NzcwMTIwNTE1NjY1.YFn9dg.lCoqMxOwpVnehLnLEjdX1Hsi0rs')
