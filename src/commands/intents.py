import discord, psutil, time, os, re
from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Intents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.bot.version = os.getenv("version")
        
    @discord.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        match = re.search(r'\bKent\b', message.content)
        if match:
            word = match.group(0)
            print(f"Found the word 'Kent': {word}")
            await message.channel.send("Kent")
        

def setup(bot):
    bot.add_cog(Intents(bot))
