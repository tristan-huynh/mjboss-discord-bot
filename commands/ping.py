import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
        
async def setup(bot):
    await bot.add_cog(ping(bot))
    
        