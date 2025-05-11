import discord, os, time, motor.motor_asyncio, logging
from discord.ext import commands
from dotenv import load_dotenv
from os import listdir

load_dotenv()

TOKEN: str = os.getenv("token")
MONGO_URI = os.getenv("mongo_uri")

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = mongo_client["discord"]

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=["/"], intents=intents, help_commmand=None)

bot.start_time = time.time()
bot.version = os.getenv("version")
bot.embed_color = 0xfca41c
bot.blacklisted_users = [
    "527972650409132033",
    "622531395134160906"
]

bot.db = db

class ColoredFormatter(logging.Formatter):
    # Define color codes for each level
    LEVEL_COLORS = {
        'DEBUG': '\033[32m',    # White
        'INFO': '\033[34m',     # Blue
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[41m', # Red background
    }
    RESET = '\033[0m'

    def format(self, record):
        levelname = record.levelname
        if levelname in self.LEVEL_COLORS:
            record.levelname = f"{self.LEVEL_COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)
    
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter('%(asctime)s %(levelname)s       %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))
    
logging.basicConfig(level=logging.INFO, handlers=[handler])

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py"):
            extension = f"src.cogs.{filename[:-3]}"
            await bot.load_extension(extension)
    try:
        await bot.change_presence(activity=discord.Game("Copilot 365 Pro+ (for work and school) (new)"))
        synced = await bot.tree.sync()
        logging.info(f"Synced {len(synced)} commands")
    except Exception as e:
        logging.critical(f"Failed to sync commands: {e}")   

# @bot.event
# async def on_interaction(interaction: discord.Interaction):
#     if interaction.type == discord.InteractionType.application_command:
#         logging.debug(f"Command {interaction.command.name} invoked by {interaction.user.name}#{interaction.user.discriminator} (ID: {interaction.user.id}) in {interaction.guild.name} (ID: {interaction.guild.id})")


bot.run(TOKEN)