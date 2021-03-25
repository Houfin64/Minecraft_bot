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

if __name__ == "__main__":
    cogs = ["cogs.shopsCog", "cogs.ordersCog"]
    for cog in cogs:
        bot.load_extension(cog)

bot.run('ODIzOTI4NzcwMTIwNTE1NjY1.YFn9dg.lCoqMxOwpVnehLnLEjdX1Hsi0rs')
