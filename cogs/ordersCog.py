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
        pass
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
