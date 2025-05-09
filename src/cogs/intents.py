from discord.ext import commands
from discord import app_commands
import discord


class Intents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if "v/s" in message.content.lower():
            await message.add_reaction("⬅️")
            await message.add_reaction("➡️")
        
        if "y/n" in message.content.lower():
            await message.add_reaction("👍")
            await message.add_reaction("👎")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Intents(bot))    