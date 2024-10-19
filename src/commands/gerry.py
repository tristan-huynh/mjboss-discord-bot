import discord, psutil, time, os
from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Gerry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.bot.version = os.getenv("version")
    
    @discord.slash_command(description="Hi")
    async def kent(self, ctx):
        user = await self.bot.fetch_user(527972650409132033)
        await user.send("Kent")
        
    #@discord.slash_command()

def setup(bot):
    bot.add_cog(Gerry(bot))

