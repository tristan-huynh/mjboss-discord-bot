import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Create a new bot instance
bot = commands.Bot(command_prefix='!')

# Get the directory path where the command files are located
commands_dir = './commands'

# Iterate over the files in the directory
for filename in os.listdir(commands_dir):
    if filename.endswith('.py'):
        # Remove the file extension to get the command name
        command_name = filename[:-3]
        
        # Load the command as an extension
        bot.load_extension(f'commands.{command_name}')

# Run the bot
bot.run(os.getenv('token'))