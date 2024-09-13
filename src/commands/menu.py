import discord
import json
from discord.ext import commands
from discord import Option
from urllib.request import urlopen, Request

API_URL = "https://api.dineoncampus.com/v1/sites/todays_menu?site_id=64872d0f351d53058416c3d5"
HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @discord.slash_command(name="menu", description="Get the menu for a specific period")
    # async def menu(ctx, period: discord.AutocompleteContext = Option(description="The period you want the menu for", choices=["Breakfast", "Lunch", "Dinner"])):
    #     response = urlopen(Request(API_URL, headers=HDR))
    #     data_json = json.loads(response.read())
    #     # location = data_json['locations'][0]['name']
    #     # meal_periods = data_json['locations'][0]['periods'][0]['name']
    #     # items = data_json['locations'][0]['periods'][0]['stations'][0]['items']
    #     # d = ""
    #     # for item in items:
    #     #     d += f"  - Name: {item['name']}, Calories: {item['calories']}, Portion: {item['portion']}\n"
    #     # embed = discord.Embed(title="Menu", color=discord.Color.blue())
    #     # embed.add_field(name="Location", value=location, inline=False)
    #     # embed.add_field(name="Meal Period", value=meal_periods, inline=False)
    #     # embed.add_field(name="Menu", value=d, inline=False)
    #     desired_stations = {"Homestyle", "500 Degrees", "Flame", "Delicious Without"}

    #     embed = discord.Embed(title="Today's Menu", color=discord.Color.blue())

    #     for location in data_json['locations']:
    #         embed.add_field(name="Location", value=location['name'], inline=False)
    #         for period_data in location['periods']:
    #             if period_data['name'].lower() == period.lower():
    #                 embed.add_field(name="Period", value=period_data['name'], inline=False)
    #                 for station in period_data['stations']:
    #                     if station['name'] in desired_stations:
    #                         station_info = f"**Station Name:** {station['name']}\n"
    #                         for item in station['items']:
    #                             station_info += f"**Item Name:** {item['name']}\n"
    #                             station_info += f"Calories: {item['calories']}\n"
    #                             station_info += f"Portion: {item['portion']}\n\n"
    #                         embed.add_field(name=station['name'], value=station_info, inline=False)

    #     await ctx.respond(embed=embed)

    async def get_period(ctx: discord.AutocompleteContext):
        period_type = ctx.options['period']
        if period_type.lower() == "Breakfast":
            return "Breakfast"
        elif period_type.lower() == "Lunch":
            return "Lunch"
        elif period_type.lower() == "Dinner":
            return "Dinner"



    @discord.slash_command(name="menu", description="Get today's menu for a specific period")
    async def menu(self, ctx: discord.ApplicationContext):
        API_URL = "https://api.dineoncampus.com/v1/sites/todays_menu?site_id=64872d0f351d53058416c3d5"
        HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        response = urlopen(Request(API_URL, headers=HDR))
        data_json = json.loads(response.read())

        # embed = discord.Embed(title="Today's Menu", description=f"Menu for {period}", color=discord.Color.blue())
        # desired_stations = {"Homestyle", "500 Degrees", "Flame", "Delicious Without"}

        # for location in data_json['locations']:
        #     embed.add_field(name="Location", value=location['name'], inline=False)
        #     for period_data in location['periods']:
        #         if period_data['name'].lower() == period.lower():
        #             embed.add_field(name="Period", value=period_data['name'], inline=False)
        #             for station in period_data['stations']:
        #                 if station['name'] in desired_stations:
        #                     station_info = f"**Station Name:** {station['name']}\n"
        #                     for item in station['items']:
        #                         station_info += f"**Item Name:** {item['name']}\n"
        #                         station_info += f"Calories: {item['calories']}\n"
        #                         station_info += f"Portion: {item['portion']}\n\n"
        #                     embed.add_field(name=station['name'], value=station_info, inline=False)

        # await ctx.respond(embed=embed)
        await ctx.respond("Hi")



def setup(bot):
    bot.add_cog(Menu(bot))