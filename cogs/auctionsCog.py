import discord
import random
from discord.ext import commands
from functions.tools import json_write, load_json, Member_Obj
import datetime

class Auctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="auctions")
    async def auctions(self, ctx):
        adict = await load_json("auctions")

        embed = discord.Embed(title="Ongoing Auctions", description="These are the auctions that haven't finished", color=random.randint(0, 16777215))
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        for elem in sdict:
            embed.add_field(name=elem, value="{} {} currently put at price {} by {}. Ends at {}".format(adict[elem]["quantity"], adict[elem]["item"], adict[elem]["cprice"], self.bot.get_user(int(adict[elem]["latest_buyer"])).name, adict[elem]["fintime"]))

        embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        await json_write("auctions", adict)

    @commands.command(name="place-bid")
    async def bid(self, ctx, auction, bid):
        pass

    @commands.command(name="start-auction")
    async def start_auction(self, ctx, name, item, quantity, starting_price, *, timescale):
        adict = await load_json("auctions")

        try: 
            year, month, day, hour, minute = timescale.split("|")
        except ValueError:
            embed = discord.Embed(title="Welp, that failed!", description="Usage: `<name> <item> <quantity(integer)> <starting price(integer)> <year|month|day|hour|minute(the time it ends)>", color=0xff0000)
            return await ctx.send(embed=embed)
        try:
            year, month, day, hour, minute, quantity, starting_price = int(quantity), int(starting_price), int(year), int(month), int(day), int(hour), int(minute)
        except ValueError:
            embed = discord.Embed(title="Welp, that failed!", description="Usage: `<name> <item> <quantity(integer)> <starting price(integer)> <year|month|day|hour|minute(the time it ends)(all integers)>", color=0xff0000)
            return await ctx.send(embed=embed)

        adict[name] = {"owner": str(ctx.author.id), "item": item, "quantity": quantity, "cprice": starting_price, "fintime": {"year": year, "month": month, "day": day, "hour": hour, "minute": minute}, "latest_buyer": str(ctx.author.id)}

        embed = discord.Embed(title="Your auction has been added.", description="It starts.... NOW!!", color=0x00ff00)
        await ctx.send(embed=embed)

        await json_write("auctions", adict)

    @commands.command(name="my-auction")
    async def myauction(self, ctx):
        auction = None
        adict = await load_json("auctions")
        for elem in adict:
            if str(ctx.author.id) == adict[elem]["owner"]:
                auction = elem
                break
        # DO STUFF WITH AUCTION, AND SEND EMBED
        if auction is not None:
            embed = discord.Embed(title="This is your ongoing auction", description="Let's see some figures!", color=random.randint(0, 16777215))
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            embed.add_field(name=elem, value="{} {} currently put at price {} by {}".format(adict[auction]["quantity"], adict[auction]["item"], adict[auction]["cprice"], self.bot.get_user(int(adict[auction]["latest_buyer"])).name))

            embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Welp, that failed!", description="You have no ongoing auctions dumbass!", color=0xff0000)
            await ctx.send(embed=embed)
        


def setup(bot):
    bot.add_cog(Auctions(bot))
