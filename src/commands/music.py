import discord, psutil, time, os
from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.bot.version = os.getenv("version")
        

def setup(bot):
    bot.add_cog(Music(bot))

