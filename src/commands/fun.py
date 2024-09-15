import discord, psutil, time, os
from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.bot.version = os.getenv("version")
        
    @discord.slash_command(description="Is IDU deleted?")
    async def idu(self, ctx):
        if (self.bot.get_guild(746844357205950606)):
            await ctx.send("IDU is not deleted.")
        else:
            await ctx.send("IDU is deleted.")
    
            
def setup(bot):
    bot.add_cog(Fun(bot))

