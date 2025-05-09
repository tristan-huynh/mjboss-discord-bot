import discord, os, time, motor.motor_asyncio
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
    "622531395134160906",
    "662367263231442965"
]

bot.db = db

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    
    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py"):
            extension = f"src.cogs.{filename[:-3]}"
            await bot.load_extension(extension)
    try:
        await bot.change_presence(activity=discord.Game("Copilot 365 Pro+ (for work and school) (new)"))
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")   



bot.run(TOKEN)