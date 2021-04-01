import discord
import random
from discord.ext import commands
from functions.tools import json_write, load_json, Member_Obj
import datetime

class Auctions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="auctions", aliases=["a"])
    async def auctions(self, ctx):
        adict = await load_json("auctions")

        embed = discord.Embed(title="Ongoing Auctions", description="These are the auctions that haven't finished", color=random.randint(0, 16777215))
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        for elem in adict:
            embed.add_field(name=elem, value="{} {} currently put at a price of {} by {}. Ends on {}/{}/{} at {}:{}".format(adict[elem]["quantity"], adict[elem]["item"], adict[elem]["cprice"], self.bot.get_user(int(adict[elem]["latest_buyer"])).name, adict[elem]["fintime"]["month"], adict[elem]["fintime"]["day"], adict[elem]["fintime"]["hour"], adict[elem]["fintime"]["minute"]))

        embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        await json_write("auctions", adict)

    @commands.command(name="place-bid", aliases=["p-bid", "pb"])
    async def bid(self, ctx, auction, bid):
        adict = await load_json("auctions")

        if auction not in adict:
            embed = discord.Embed(title="Welp, that failed!", description="That auction doesn't exist!", color=0xff0000)
            return await ctx.send(embed=embed)
        try:
            bid = int(bid)
        except ValueError:
            embed = discord.Embed(title="Welp, that failed!", description="Your bid has to be an integer!", color=0xff0000)
            return await ctx.send(embed=embed)
        if bid < int(adict[auction]["cprice"]):
            embed = discord.Embed(title="Welp, that failed!", description="Your bid has to be larger than the current one!", color=0xff0000)
            return await ctx.send(embed=embed)
        
        adict[auction]["cprice"] = str(bid)

        embed = discord.Embed(title="Success!", description="Your bid has been approved and set!", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name="start-auction", aliases=["sa, st-auc"])
    async def start_auction(self, ctx, name, item, quantity, starting_price, *, timescale):
        adict = await load_json("auctions")

        if name in adict:
            embed = discord.Embed(title="Welp, that failed!", description="Choose a unique auction name", color=0xff0000)
            return await ctx.send(embed=embed)
        for elem in adict:
            if adict[elem]["owner"] == str(ctx.author.id):
                embed = discord.Embed(title="Welp, that failed!", description="You already have an ongoing auction, do <£close-auction> to close it.", color=0xff0000)
                return await ctx.send(embed=embed)

        try: 
            month, day, hour, minute = timescale.split("|")
        except ValueError:
            embed = discord.Embed(title="Welp, that failed!", description="Usage: `<name> <item> <quantity(integer)> <starting price(integer)> <month|day|hour|minute(the time it ends)(all integers)>`", color=0xff0000)
            return await ctx.send(embed=embed)
        try:
            month, day, hour, minute, quantity, starting_price = int(month), int(day), int(hour), int(minute), int(quantity), int(starting_price)
        except ValueError:
            embed = discord.Embed(title="Welp, that failed!", description="Usage: `<name> <item> <quantity(integer)> <starting price(integer)> <month|day|hour|minute(the time it ends)(all integers)>`", color=0xff0000)
            return await ctx.send(embed=embed)

        adict[name] = {"owner": str(ctx.author.id), "item": item, "quantity": quantity, "cprice": str(starting_price), "fintime": {"month": month, "day": day, "hour": hour, "minute": minute}, "latest_buyer": str(ctx.author.id)}

        embed = discord.Embed(title="Your auction has been added.", description="It starts.... NOW!!", color=0x00ff00)
        await ctx.send(embed=embed)

        await json_write("auctions", adict)
    
    @commands.command(name="close-auction", aliases=["ca, cl-auc"])
    async def close_auction(self, ctx):
        adict = await load_json("auctions")

        for elem in adict:
            if adict[elem]["owner"] == str(ctx.author.id):

                embed=discord.Embed(title="Success!", description="Your auction has been closed, {} has bought {} {} for {}".format(self.bot.get_user(int(adict[elem]["latest_buyer"])).name, adict[elem]["quantity"], adict[elem]["item"], adict[elem]["cprice"]), color=random.randint(0, 16777215))

                del adict[elem]

                await json_write("auctions", adict)

                return await ctx.send(embed=embed)

        embed = discord.Embed(title="Welp, that failed!", description="You don't have an open auction!", color=0xff0000)
        await ctx.send(embed=embed)

    @commands.command(name="my-auction", aliases=["ma, my-auc"])
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
            embed.add_field(name=elem, value="{} {} currently put at a price of {} by {}".format(adict[auction]["quantity"], adict[auction]["item"], adict[auction]["cprice"], self.bot.get_user(int(adict[auction]["latest_buyer"])).name))

            embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Welp, that failed!", description="You have no ongoing auctions dumbass!", color=0xff0000)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Auctions(bot))
