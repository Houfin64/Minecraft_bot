import discord
import random
from discord.ext import commands
from functions.tools import json_write, load_json, Member_Obj
import datetime

class Orders(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oops", description="looks like you forgot an argument!", color=0xff0000)
            await ctx.send(embed=embed)
        elif not isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title=str(error), description="Oh oh, crash!", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(name="place-order", aliases=["po", "pla-ord"])
    async def place_order(self, ctx, shop, *, argument):
        udict = await load_json("users")
        sdict = await load_json("shops")
        iodict = await load_json("orders")
        oodict = await load_json("out_orders")

        if "|" not in argument:
            embed = discord.Embed(title="Welp, that failed!", description="Syntax: `£place-order <shop> <item>|<quantity>`", color=0xff0000)
            return await ctx.send(embed=embed)

        item, quantity = argument.partition("|")[0], argument.partition("|")[2]

        orderer = str(ctx.author.id)
        if shop not in sdict:
            embed = discord.Embed(title="Welp that failed!", description="That shop doesn't exist. use `£shops` to see the existing ones", color=0xff0000)
            return await ctx.send(embed=embed)
        if item not in sdict[shop]["items"]:
            embed = discord.Embed(title="Welp that failed!", description="That item doesn't exist. use `£shop <user>` to see the existing ones", color=0xff0000)
            return await ctx.send(embed=embed)
        try: 
            if item in oodict[orderer]:
                embed = discord.Embed(title="Welp that failed!", description="You already have an outstanding order of that, `£revoke-order` to make a new one", color=0xff0000)
                return await ctx.send(embed=embed)
        except KeyError:
            pass
        try:
            tprice = int(quantity) * int(sdict[shop]["items"][item])
        except ValueError:
            embed = discord.Embed(title="Welp that failed!", description="usage: `£place-order <shop> <item>|<quantity(integer)>", color=0xff0000)
            return await ctx.send(embed=embed)
        
        orderee = sdict[shop]["owner"]

        if orderee not in iodict:
            iodict[orderee] = {item: {"orderer": orderer, "tprice": tprice, "quantity": quantity, "shop": shop, "item": item}}
        else:
            iodict[orderee][item] = {"orderer": orderer, "tprice": tprice, "quantity": quantity, "shop": shop, "item": item}
        if orderer not in oodict:
            oodict[orderer] = {item: {"orderee": orderee, "tprice": tprice, "quantity": quantity, "shop": shop, "item": item}}
        else:
            oodict[orderer][item] = {"orderee": orderee, "tprice": tprice, "quantity": quantity, "shop": shop, "item": item}

        await self.bot.get_user(int(orderee)).create_dm()

        embed = discord.Embed(title="An Order has been placed with your shop", description="For {} {}s for a total price of {}".format(quantity, item, tprice), color=0x00ff00)
        await self.bot.get_user(int(orderee)).dm_channel.send(embed=embed)

        embed = discord.Embed(title="Succes!", description="Your order has been placed", color=0x00ff00)
        await ctx.send(embed=embed)

        await json_write("orders", iodict)
        await json_write("out_orders", oodict)

        # NOTE:  DM will be sent automatically when order is placed, and a second DM will be sent when revoked to apologise for useless DM

    @commands.command(name="revoke-order", aliases=["ro", "rev-ord"])
    async def revoke_order(self, ctx, order):
        udict = await load_json("users")
        sdict = await load_json("shops")
        iodict = await load_json("orders")
        oodict = await load_json("out_orders")

        if str(ctx.author.id) not in oodict:
            embed = discord.Embed(title="Welp that failed!", description="You don't have any outgoing orders", color=0xff0000)
            return await ctx.send(embed=embed)
        if order not in oodict[str(ctx.author.id)]:
            embed = discord.Embed(title="Welp that failed!", description="You don't have an outstanding order of that item", color=0xff0000)
            return await ctx.send(embed=embed)

        orderee = oodict[str(ctx.author.id)][order]["orderee"]
        quantity = oodict[str(ctx.author.id)][order]["quantity"]

        del oodict[str(ctx.author.id)][order]
        del iodict[orderee][order]

        embed = discord.Embed(title="Succes!", description="Your order has been revoked", color=0x00ff00)
        await ctx.send(embed=embed)

        await self.bot.get_user(int(orderee)).create_dm()

        embed = discord.Embed(title="An order has been revoked", description="Sorry for previous ping, but the order made for {} {} has now been revoked by {}".format(quantity, order, self.bot.get_user(int(orderee)).name), color=0xff0000)
        await self.bot.get_user(int(orderee)).dm_channel.send(embed=embed)

        await json_write("orders", iodict)
        await json_write("out_orders", oodict)

    @commands.command(name="complete-order", aliases=["co", "comp-ord"])
    async def complete_order(self, ctx, order):
        udict = await load_json("users")
        sdict = await load_json("shops")
        iodict = await load_json("orders")
        oodict = await load_json("out_orders")

        if str(ctx.author.id) not in iodict:
            embed = discord.Embed(title="Welp that failed!", description="You don't have any incoming orders", color=0xff0000)
            return await ctx.send(embed=embed)
        if order not in iodict[str(ctx.author.id)]:
            embed = discord.Embed(title="Welp that failed!", description="You don't have an incoming order of that item", color=0xff0000)
            return await ctx.send(embed=embed)

        orderer = iodict[str(ctx.author.id)][order]["orderer"]
        quantity = iodict[str(ctx.author.id)][order]["quantity"]

        del iodict[str(ctx.author.id)][order]
        del oodict[orderer][order]

        embed = discord.Embed(title="Succes!", description="Your order has been completed", color=0x00ff00)
        await ctx.send(embed=embed)

        await self.bot.get_user(int(orderer)).create_dm()

        embed = discord.Embed(title="An order has been completed", description="Your order made for {} {} has now been completed by {}".format(quantity, order, self.bot.get_user(int(orderer)).name), color=0x00ff00)
        await self.bot.get_user(int(orderer)).dm_channel.send(embed=embed)

        await json_write("orders", iodict)
        await json_write("out_orders", oodict)

    @commands.command(name="outgoing-orders", aliases=["oo", "out-ord"])
    async def my_orders(self, ctx, *, profiles: Member_Obj = None):
        if profiles == None:
            profiles = [ctx.author]
        if len(profiles) > 1:
            embed = discord.Embed(description="Be more specific for goodness's sake!", color=0xff0000)
            return await ctx.send(embed=embed)
        user = profiles[0]

        iodict = await load_json("orders")
        oodict = await load_json("out_orders")
        sdict = await load_json("shops")
        udict = await load_json("users")

        shop_name = udict[str(user.id)]
        shop_description = sdict[shop_name]["description"]

        embed = discord.Embed(title=shop_name, description=shop_description, color=random.randint(0, 16777215))
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        for elem in oodict[str(user.id)]:
            embed.add_field(name=elem, value="{} | {}".format(oodict[str(user.id)][elem]["quantity"], oodict[str(user.id)][elem]["tprice"]))
        embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="incoming-orders", aliases=["io", "in-ord"])
    async def incoming_orders(self, ctx, *, profiles: Member_Obj = None):
        if profiles == None:
            profiles = [ctx.author]
        if len(profiles) > 1:
            embed = discord.Embed(description="Be more specific for goodness's sake!", color=0xff0000)
            return await ctx.send(embed=embed)
        user = profiles[0]

        iodict = await load_json("orders")
        oodict = await load_json("out_orders")
        sdict = await load_json("shops")
        udict = await load_json("users")

        shop_name = udict[str(user.id)]
        shop_description = sdict[shop_name]["description"]

        embed = discord.Embed(title=shop_name, description=shop_description, color=random.randint(0, 16777215))
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        for elem in iodict[str(user.id)]:
            embed.add_field(name=elem, value="{} | {}".format(iodict[str(user.id)][elem]["quantity"], iodict[str(user.id)][elem]["tprice"]))
        embed.set_footer(text=f"requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        while 1:
            if datetime.seconds == 0:
                self.auction_loop.start()
                break

    @tasks.loop(60)
    async def auction_loop(self):
        adict = await load_json("auctions")

        for elem in adict:
            if [datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute] == adict[elem]["fintime"]:
                embed = discord.Embed(title="Auction Has Ended!", description="the auction {} by {} for {} {} has been sold to {} for a price of {}!".format(adict[elem]["name"], self.bot.get_user(int(adict[elem]["ownwer"])).name, adict[elem]["quantity"], adict[elem]["item"], self.bot.get_user(int(adict[elem]["latest_buyer"])).name, adict[elem]["cprice"]), color=random.randint(0, 16777215))
                await ctx.send(embed=embed)

                await self.bot.get_user(int(adict[elem]["owner"])).create_dm()

                embed = discord.Embed(title="Your auction has ended", description="your auction {} for {} {} has been sold to {} for a price of {}!".format(adict[elem]["name"], adict[elem]["quantity"], adict[elem]["item"], self.bot.get_user(int(adict[elem]["latest_buyer"])).name, adict[elem]["cprice"])".format(quantity, order, self.bot.get_user(int(orderee)).name), color=0xff0000)
                await self.bot.get_user(int(adict[elem]["owner"])).dm_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Orders(bot))
