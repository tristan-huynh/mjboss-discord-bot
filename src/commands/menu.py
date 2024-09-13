import discord
import json
from discord.ext import commands
from urllib.request import urlopen

API_URL = "https://api.dineoncampus.com/v1/sites/todays_menu?site_id=64872d0f351d53058416c3d5"

class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Show the bot's status")
    async def menu(self, ctx: discord.ApplicationContext):
        response = urlopen(API_URL)
        data_json = json.loads(response.read())
        await ctx.respond(data_json);

def setup(bot):
    bot.add_cog(Menu(bot))