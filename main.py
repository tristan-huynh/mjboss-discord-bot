import os
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime, timezone

load_dotenv()

TOKEN: str = os.getenv("token")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

def print_with_timestamp(message: str):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
    print(f'[{timestamp}] {message}')

@bot.event
async def on_ready():
    print_with_timestamp(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="/help"))

async def load_extensions():
    for filename in os.listdir('./src/commands/'):
        if filename.endswith('.py'):
            bot.load_extension(f'src.commands.{filename[:-3]}')
            print_with_timestamp(f'Loaded {filename[:-3]}')

async def main():
    await load_extensions()
    await bot.start(TOKEN)

asyncio.run(main())
