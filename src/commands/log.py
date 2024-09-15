import discord
from discord.ext import commands
import psutil
import time


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.bot.version = "1.0.0"
        

def setup(bot):
    bot.add_cog(Log(bot))

