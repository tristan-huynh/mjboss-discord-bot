import os
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN: str = os.getenv("token")

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

async def on_ready():
    print(f'Logged in as {bot.user}')

async def load():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')
            print(f'Loaded {filename[:-3]}')
        
async def main():
    await load()
    await bot.start(TOKEN)
    await on_ready()
    await bot.tree.sync()

asyncio.run(main())