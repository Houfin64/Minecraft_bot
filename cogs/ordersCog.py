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

        orderer = str(ctx.author.id)
        if shop not in sdict:
            embed = discord.Embed(title="Welp that failed!", description="That shop doesn't exist. use `£shops` to see the existing ones", color=0xff0000)
            return await ctx.send(embed=embed)
        if item not in sdict[shop]["items"]:
            embed = discord.Embed(title="Welp that failed!", description="That item doesn't exist. use `£shop <user>` to see the existing ones", color=0xff0000)
            return await ctx.send(embed=embed)
        try:
            tprice = int(quantity) * int(sdict[shop]["items"][item])
        except ValueError:
            embed = discord.Embed(title="Welp that failed!", description="usage: `£place-order <shop> <item> <quantity(integer)>", color=0xff0000)
            return await ctx.send(embed=embed)
        
        orderee = sdict[shop]["owner"]

        iodict[orderee] = {"orderer": orderer, "tprice": tprice, "quantity": quantity, "shop": shop, "item": item}
        oodict[orderer] = {"orderee": orderee, "tprice": tprice, "quantity": quantity, "shop": shop, "item": item}

        await self.bot.get_user(int(orderee)).create_dm()

        embed = discord.Embed(title="An Order has been placed with your shop", description="For {} {}s for a total price of {}".format(quantity, item, tprice), colour=0x00ff00)
        await self.bot.get_user(int(orderee)).dm_channel.send(embed=embed)

        await json_write("orders", iodict)
        await json_write("out_orders", oodict)

        # NOTE:  DM will be sent automatically when order is placed, and a second DM will be sent when revoked to apologise for useless DM

    @commands.command(name="revoke-order")
    async def revoke_order(self, ctx, order):
        pass

    @commands.command(name="outgoing-orders")
    async def my_orders(self, ctx):
        pass

    @commands.command(name="incoming-orders")
    async def shop_orders(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Orders(bot))
