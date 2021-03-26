import discord
import random
from discord.ext import commands
from functions.tools import json_write, load_json, Member_Obj

class Orders(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Oops", description="looks like you forgot an argument!", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(name="place-order")
    async def place_order(self, ctx, shop, item, quantity):
        udict = await load_json("users")
        sdict = await load_json("shops")
        iodict = await load_json("orders")
        oodict = await load_json("out_orders")

        if "|" not in argument:
            embed = discord.Embed(title="Welp, that failed!", description="Syntax: `£place-order <shop>|<item>|<quantity>`", color=0xff0000)
            return await ctx.send(embed=embed)

        shop, item, quantity = argument.partition("|")[0], argument.partition("|")[2], argument.partition("|")[4]

        orderer = str(ctx.author.id)
        if shop not in sdict:
            embed = discord.Embed(title="Welp that failed!", description="That shop doesn't exist. use `£shops` to see the existing ones", color=0xff0000)
            return await ctx.send(embed=embed)
        if item not in sdict[shop]["items"]:
            embed = discord.Embed(title="Welp that failed!", description="That item doesn't exist. use `£shop <user>` to see the existing ones", color=0xff0000)
            return await ctx.send(embed=embed)
        if item in oodict[orderer]:
            embed = discord.Embed(title="Welp that failed!", description="You already have an outstanding order of that, `£revoke-order` to make a new one", color=0xff0000)
            return await ctx.send(embed=embed)
        try:
            tprice = int(quantity) * int(sdict[shop]["items"][item])
        except ValueError:
            embed = discord.Embed(title="Welp that failed!", description="usage: `£place-order <shop> <item> <quantity(integer)>", color=0xff0000)
            return await ctx.send(embed=embed)
        
        orderee = sdict[shop]["owner"]

        if orderee not in iodict:
            iodict[orderee] = {"item": {"orderer": orderer, "tprice": tprice, "quantity": quantity, "shop": shop, "item": item}}
        if orderer not in oodict:
            oodict[orderer] = {"item": {"orderee": orderee, "tprice": tprice, "quantity": quantity, "shop": shop, "item": item}}

        await self.bot.get_user(int(orderee)).create_dm()

        embed = discord.Embed(title="An Order has been placed with your shop", description="For {} {}s for a total price of {}".format(quantity, item, tprice), color=0x00ff00)
        await self.bot.get_user(int(orderee)).dm_channel.send(embed=embed)

        embed = discord.Embed(title="Succes!", description="Your order has been placed", color=0x00ff00)
        await ctx.send(embed=embed)

        await json_write("orders", iodict)
        await json_write("out_orders", oodict)

        # NOTE:  DM will be sent automatically when order is placed, and a second DM will be sent when revoked to apologise for useless DM

    @commands.command(name="revoke-order")
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

        orderee = oodict[ctx.author.id]["orderee"]
        del oodict[ctx.author.id][order]
        del iodict[int(orderee)][order]

        embed = discord.Embed(title="Succes!", description="Your order has been revoked", color=0x00ff00)
        await ctx.send(embed=embed)

        await self.bot.get_user(int(orderee)).create_dm()

        embed = discord.Embed(title="An order has been revoked", description="Sorry for previous ping, but the order made has now been revoked by the orderer".format(quantity, item, tprice), color=0xff0000)
        await self.bot.get_user(int(orderee)).dm_channel.send(embed=embed)

    @commands.command(name="outgoing-orders")
    async def my_orders(self, ctx):
        pass

    @commands.command(name="incoming-orders")
    async def shop_orders(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Orders(bot))
