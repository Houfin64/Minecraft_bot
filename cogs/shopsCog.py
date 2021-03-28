import discord
import random
from discord.ext import commands
from functions.tools import json_write, load_json, Member_Obj

class Shops(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create-shop", aliases=["cs", "cre-s"])
    async def create_shop(self, ctx, *, argument):

        sdict = await load_json("shops")
        udict = await load_json("users")

        if "|" not in argument:
            embed = discord.Embed(title="Welp, that failed!", description="Syntax: `£create-shop <colour> <shop-name>|<description>`", color=0xff0000)
            return await ctx.send(embed=embed)

        name, description = argument.partition("|")[0], argument.partition("|")[2]

        owner = ctx.author.id
        
        if str(owner) in udict:
            embed = discord.Embed(title="Welp that failed!", description="You can't have more than 1 shop, add items instead.  \nIf you want to delete your shop do `£remove-shop` instead, and i will take yor stall down.", color=0xff0000)
            return await ctx.send(embed=embed)
        if name in sdict:
            embed = discord.Embed(title="Welp that failed", description="To avoid errors, please have a unique shop name", color=0xff0000)
            return await ctx.send(embed=embed)

        embed = discord.Embed(title="KK, Thanks", description="I've added you to the shop list :)! do `£add-item` to add items to your shop.", color=random.randint(0, 16777215))
        await ctx.send(embed=embed)

        udict[str(ctx.author.id)] = name
        sdict[name] = {"owner": str(owner), "description": description, "items": {}, "name": name}

        await json_write("shops", sdict)
        await json_write("users", udict)

    @commands.command(name="remove-shop", aliases=["rs", "rem-s"])
    async def remove_shop(self, ctx):
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

    @commands.command(name="add-item", aliases=["ai", "add-i"])
    async def add_item(self, ctx, *, argument):

        if "|" not in argument:
            embed = discord.Embed(title="Welp, that failed!", description="Syntax: `£add-item <item-name>|<price>`", color=0xff0000)
            return await ctx.send(embed=embed)

        item, price = argument.partition("|")[0], argument.partition("|")[2]

        sdict = await load_json("shops")
        udict = await load_json("users")

        try:
            price = int(price)
        except ValueError:
            embed = discord.Embed(title="Welp, that failed!", description="Usage:  `£add-item <item>|<price(integer)>`", color=0xff0000)
            return await ctx.send(embed=embed)
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

    @commands.command(name="remove-item", aliases=["ri", "rem-i"])
    async def remove_item(self, ctx, item):
        sdict = await load_json("shops")
        udict = await load_json("users")
        try:
            del sdict[udict[str(ctx.author.id)]]["items"][item]
        except KeyError:
            embed = discord.Embed(title="Welp, that failed!", description="You don't sell that item :)", color=0xff0000)
            return await ctx.send(embed=embed)
        
        embed = discord.Embed(title="That's you done :)", description="Your item has been removed from your shop", color=0x00ff00)
        await ctx.send(embed=embed)

        await json_write("shops", sdict)

    @commands.command(name="shops", aliases=["ls", "list-shops", "stalls"])
    async def shops(self, ctx):
        sdict = await load_json("shops")

        embed = discord.Embed(title="Shops", description="These are the shops that people own", color=random.randint(0, 16777215))
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        for elem in sdict:
            embed.add_field(name=elem, value=self.bot.get_user(int(sdict[elem]["owner"])).name)

        embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

        await json_write("shops", sdict)

    @commands.command(name="shop", aliases=["s", "stall"])
    async def shop(self, ctx, *, profiles: Member_Obj = None):
        if profiles == None:
            profiles = [ctx.author]
        if len(profiles) > 1:
            embed = discord.Embed(description="Be more specific for goodness's sake!", color=0xff0000)
            return await ctx.send(embed=embed)
        user = profiles[0]


        sdict = await load_json("shops")
        udict = await load_json("users")

        if str(user.id) not in udict:
            embed = discord.Embed(title="Welp, that failed!", description="You need to `£create-shop` to be able to see your shop :)", color = 0xff0000)
            return await ctx.send(embed=embed)

        embed = discord.Embed(title=sdict[udict[str(user.id)]]["name"], description=sdict[udict[str(user.id)]]["description"], color=sdict[str(user.id)["colour"]])
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        for elem in sdict[udict[str(user.id)]]["items"]:
            embed.add_field(name=elem, value=sdict[udict[str(user.id)]]["items"][elem])
        embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(name="debts", aliases=["debt", "d"])
    async def debts(self, ctx):
        iodict = await load_json("orders")
        oodict = await load_json("out_orders")
        sdict = await load_json("shops")
        udict = await load_json("users")

        tdebt = 0
        embed = discord.Embed(title="Debts",  description="To be paid to you", color=random.randint(0, 16777215))
        for debt in iodict[str(ctx.author.id)]:
            orderer = self.bot.get_user(int(iodict[str(ctx.author.id)][debt]["orderer"])).name
            payment = iodict[str(ctx.author.id)][debt]["tprice"]
            tdebt += payment
            embed.add_field(name=orderer, value="{} for {} {}".format(payment, iodict[str(ctx.author.id)][debt]["quantity"], iodict[str(ctx.author.id)][debt]["item"]))
        embed.add_field(name="Total debts To be Paid", value=str(tdebt))
        await ctx.send(embed=embed)

    
    @commands.command(name="my-debts", aliases=["md", "mydebt"])
    async def mydebts(self, ctx):
        iodict = await load_json("orders")
        oodict = await load_json("out_orders")
        sdict = await load_json("shops")
        udict = await load_json("users")

        tdebt = 0
        embed = discord.Embed(title="Debts",  description="To be paid by you", color=random.randint(0, 16777215))
        for debt in oodict[str(ctx.author.id)]:
            orderee = self.bot.get_user(int(oodict[str(ctx.author.id)][debt]["orderee"])).name
            payment = oodict[str(ctx.author.id)][debt]["tprice"]
            tdebt += payment
            embed.add_field(name=orderee, value="{} for {} {}".format(payment, oodict[str(ctx.author.id)][debt]["quantity"], oodict[str(ctx.author.id)][debt]["item"]))
        embed.add_field(name="Total debts To be Paid", value=str(tdebt))
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Shops(bot))
