import discord, os, psutil, time, json
from discord.ext import commands
from dotenv import load_dotenv
from urllib.request import urlopen, Request

load_dotenv()
OPENWEATHER_API_KEY: str = os.getenv("openweathertoken")

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.bot.version = os.getenv("version")

    @discord.slash_command(description="Show the bot's status")
    async def status(self, ctx: discord.ApplicationContext):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        uptime = time.time() - self.start_time
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))
        server_count = len(self.bot.guilds)

        embed = discord.Embed(title="Status", color=discord.Color.blue())
        embed.add_field(name="CPU Usage", value=f"{cpu_usage}%", inline=True)
        embed.add_field(name="Memory Usage", value=f"{memory_info.percent}%", inline=True)
        embed.add_field(name="Uptime", value=uptime_str, inline=True)
        embed.add_field(name="Servers", value=server_count, inline=True)
        embed.add_field(name="Websocket Latency", value=f"0 ms", inline=True)
        embed.add_field(name="Client Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")

        await ctx.respond(embed=embed)
        
    @discord.slash_command(description="Make the bot say something")
    async def say(self, ctx: discord.ApplicationContext, message: str):
        await ctx.respond("Message successfully sent!", ephemeral=True)
        await ctx.send(message)
        
    @discord.slash_command(description="Get a user info")
    async def userinfo(self, ctx: discord.ApplicationContext, user: discord.User):
        embed = discord.Embed(title="User Info", color=discord.Color.blue())
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Bot", value=user.bot, inline=True)
        embed.add_field(name="Created At", value=user.created_at, inline=True)
        embed.set_thumbnail(url=user.avatar.url)
        
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        await ctx.respond(embed=embed)
        
    @discord.slash_command(description="Get a users avatar")
    async def avatar(self, ctx: discord.ApplicationContext, user: discord.User):
        embed = discord.Embed(title="Avatar", color=discord.Color.blue())
        embed.set_image(url=user.avatar.url)
        
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        await ctx.respond(embed=embed)
        
    @discord.slash_command(description="Get server member count")
    async def membercount(self, ctx: discord.ApplicationContext):
        bot_count = sum(member.bot for member in ctx.guild.members)
        user_count = len(ctx.guild.members) - bot_count
        embed = discord.Embed(title="Member Count", color=discord.Color.blue())
        embed.add_field(name="Bot Count", value=bot_count, inline=True)
        embed.add_field(name="User Count", value=user_count, inline=True)
        
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        await ctx.respond(embed=embed)
        
    @discord.slash_command(description="Get server info")
    async def serverinfo(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="Server Info", color=discord.Color.blue())
        embed.add_field(name="Name", value=ctx.guild.name, inline=True)
        embed.add_field(name="ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
        embed.add_field(name="Created At", value=ctx.guild.created_at, inline=True)
        embed.add_field(name="Member Count", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Role Count", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="Channel Count", value=len(ctx.guild.channels), inline=True)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        await ctx.respond(embed=embed)
        
    @discord.slash_command(description="Get weather info")
    async def weather(self, ctx: discord.ApplicationContext, city: str):
        city = city.replace(" ", "%20")
        API_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
        HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        try:
            reponse = urlopen(Request(API_URL, headers=HDR))
            data_json = json.loads(reponse.read())
            
            embed = discord.Embed(title=f"{data_json['name']}, {data_json['sys']['country']}", color=discord.Color.blue())
            embed.add_field(name="Condition", value=data_json['weather'][0]['description'], inline=True)
            embed.add_field(name="Temperature", value=data_json['main']['temp'], inline=True)
            embed.add_field(name="Feels Like", value=data_json['main']['feels_like'], inline=True)
            embed.add_field(name="Humidity", value=f"{data_json['main']['humidity']}%", inline=True)
            embed.add_field(name="Wind Speed", value=data_json['wind']['speed'], inline=True)
            embed.add_field(name="Pressure", value=data_json['main']['pressure'], inline=True)
            embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{data_json['weather'][0]['icon']}.png")
            
            embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
            await ctx.respond(embed=embed)
        except:
            await ctx.respond("Failed to get weather info.", ephemeral=True)
        
        
    

def setup(bot):
    bot.add_cog(Utils(bot))
