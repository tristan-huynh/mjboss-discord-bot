from discord.ext import commands
from discord import app_commands, PartialEmoji
import discord, psutil, time, logging, re, aiohttp

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def blacklist_check():
        async def predicate(interaction: discord.Interaction) -> bool:
            if str(interaction.user.id) in interaction.client.blacklisted_users:
                raise app_commands.CheckFailure("You are currently restricted from accessing this system's commands. Command usage may be monitored to detect unauthorized activity. Unauthorized attempts to access, obtain, upload, modify, change, and/or delete information on this system are strictly prohibited and are subject to criminal prosecution under 18 U.S.C. § 1030, and other applicable statutes, which may result in fines and imprisonment.\n\nThis event has been recorded. If you believe this restriction is in error or wish to appeal, please contact the system administrator.")
            return True
        return app_commands.check(predicate)
    
    @app_commands.command(name="status", description="Bot status")
    @blacklist_check()
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        uptime = time.time() - self.bot.start_time
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))
        server_count = len(self.bot.guilds)
        
        embed = discord.Embed(title="System Status", color=self.bot.embed_color)
        embed.add_field(name="CPU Usage", value=f"{cpu_usage}%", inline=True)
        embed.add_field(name="Memory Usage", value=f"{memory_info.used / (1024 ** 3):.2f} GB", inline=True)
        embed.add_field(name="Uptime", value=uptime_str, inline=True)
        embed.add_field(name="Client Latency", value=f"{round(self.bot.latency)}ms", inline=True)
        embed.add_field(name="Websocket Latency", value=f"{self.bot.ws.latency * 1000:.2f}ms", inline=True)
        embed.add_field(name="Server Count", value=server_count, inline=True)
        embed.timestamp = discord.utils.utcnow()
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        await interaction.followup.send(embed=embed, ephemeral=False)
        
    @app_commands.command(name="avatar", description="Get the avatar of a user or the server icon")
    @app_commands.describe(
        user="The user to get the avatar of (leave blank to use your own avatar)",
        server="Set to true to get the user's server icon instead of a user avatar"
    )
    @blacklist_check()
    async def avatar(self, interaction: discord.Interaction, user: discord.User = None, server: bool = False):
        await interaction.response.defer(ephemeral=False)
        if server:
            member = interaction.guild.get_member(user.id) if user else interaction.guild.get_member(interaction.user.id)
            if member is None:
                return await interaction.followup.send("User not found in this server.", ephemeral=False)

            if member.guild_avatar:
                avatar_url = member.guild_avatar.url
                title = f"{member.name}'s Server-Specific Avatar"
            else:
                avatar_url = member.avatar.url
                title = f"{member.name}'s Global Avatar (No server-specific avatar set)"
        else:
            target = user or interaction.user
            avatar_url = target.avatar.url
            title = f"{target.name}'s Avatar"
        embed = discord.Embed(title=title, color=self.bot.embed_color)
        embed.set_image(url=avatar_url)
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        await interaction.followup.send(embed=embed, ephemeral=False)
    
    
    @app_commands.command(name="membercount", description="Get the number of members in the server")
    @blacklist_check()
    async def membercount(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        member_count = interaction.guild.member_count
        
        embed = discord.Embed(title="Member Count", color=self.bot.embed_color)
        embed.add_field(name="Total Members", value=member_count, inline=True)
        
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        await interaction.followup.send(embed=embed, ephemeral=False)
        
    @app_commands.command(name="serverinfo", description="Get information about the server")
    @blacklist_check()
    async def serverinfo(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        embed = discord.Embed(title=f"{interaction.guild.name} Info", color=self.bot.embed_color)
        embed.add_field(name="Owner", value=interaction.guild.owner.mention, inline=True)
        embed.add_field(name="Server ID", value=interaction.guild.id, inline=True)
        embed.add_field(name="Created", value=interaction.guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Total Members", value=interaction.guild.member_count, inline=True)
        embed.add_field(name="Total Channels", value=len(interaction.guild.channels), inline=True)
        embed.add_field(name="Total Roles", value=len(interaction.guild.roles), inline=True)
        embed.add_field(name="Server Boost Level", value=interaction.guild.premium_tier, inline=True)
        embed.add_field(name="Boost Count", value=interaction.guild.premium_subscription_count, inline=True)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        embed.timestamp = discord.utils.utcnow()
        await interaction.followup.send(embed=embed, ephemeral=False)

    @app_commands.command(name="poll", description="Create a poll")
    @app_commands.describe(question="The question for the poll")
    @blacklist_check()
    async def poll(self, interaction: discord.Interaction, question: str, 
                   option1: str,
                   option2: str,
                   option3: str = None,
                   option4: str = None,
                   option5: str = None):
        await interaction.response.defer(ephemeral=False)
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
        options = [option1, option2, option3, option4, option5]
        options = [option for option in options if option] 

        description = ""
        for i, option in enumerate(options):
            description += f"{emojis[i]} {option}\n\n"

        embed = discord.Embed(
            title=question,
            description=description,
            color=self.bot.embed_color
        )
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        embed.timestamp = discord.utils.utcnow()
        # Send the embed
        poll_message = await interaction.followup.send(embed=embed)

        # Add reactions based on the number of options
        for i in range(len(options)):
            await poll_message.add_reaction(emojis[i])
        
    @app_commands.command(name="ping", description="Get the bot's ping")
    @blacklist_check()
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        embed = discord.Embed(title="Pong!", color=self.bot.embed_color)
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        await interaction.followup.send(embed=embed, ephemeral=False)
    
    @app_commands.command(name="say", description="Make the bot say something")
    @app_commands.describe(message="The message to send")
    @blacklist_check()
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.guild_permissions.administrator:
            await interaction.followup.send("Message sent!", ephemeral=True)
            await interaction.channel.send(message)
        else:
            await interaction.followup.send("You do not have permission to use this command.", ephemeral=True)
            return

    @app_commands.command(name="userinfo", description="Get help with the bot")
    @app_commands.describe(user="The user to get the info of")
    @blacklist_check()
    async def userinfo(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer(ephemeral=False)
        
        embed = discord.Embed(title=f"{user.name}'s Info", color=self.bot.embed_color)
        embed.add_field(name="Discriminator", value=user.name, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Highest Role", value=user.top_role.mention, inline=True)
        embed.add_field(name="Bot", value="Yes" if user.bot or (str(user.id) in self.bot.blacklisted_users) else "No", inline=True)
        embed.set_thumbnail(url=user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        await interaction.followup.send(embed=embed, ephemeral=False)

    @app_commands.command(name="steal", description="Steal an emoji from another server")
    @app_commands.describe(emoji="The emoji to steal")
    @blacklist_check()
    async def steal(self, interaction: discord.Interaction, emoji: str):
        await interaction.response.defer(ephemeral=False)

        if not interaction.user.guild_permissions.manage_emojis:
            return await interaction.followup.send("You do not have permission to use this command.", ephemeral=False)

        # parse "<:name:id>" or "<a:name:id>"
        m = re.match(r"<(a?):([^:]+):(\d+)>$", emoji)
        if not m:
            return await interaction.followup.send(
                "Invalid emoji format. Use `<:name:id>` or `<a:name:id>`.",
                ephemeral=False
            )

        animated, name, eid = m.groups()
        ext = "gif" if animated else "png"
        url = f"https://cdn.discordapp.com/emojis/{eid}.{ext}"

        # fetch the image bytes
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await interaction.followup.send("Emoji not found on CDN.", ephemeral=False)
                data = await resp.read()

        # create it in *this* guild
        try:
            new_emoji = await interaction.guild.create_custom_emoji(
                name=name,
                image=data
            )
        except discord.HTTPException as e:
            logging.exception("create_custom_emoji failed")
            return await interaction.followup.send("Failed to add emoji to this server.", ephemeral=False)

        await interaction.followup.send(f"✅ Added `{new_emoji.name}`", ephemeral=False)
            
    @userinfo.error
    @say.error
    @ping.error
    @poll.error
    @serverinfo.error
    @membercount.error    
    @avatar.error    
    @status.error
    async def permission_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, commands.MissingPermissions):
            msg = "You do not have permission to use this command."
        elif isinstance(error, app_commands.CheckFailure):
            msg = str(error)
        else:
            msg = "An error occurred. Please try again later."

        if not msg:
            msg = "An unknown error occurred."
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=False)
        else:
            await interaction.response.send_message(msg, ephemeral=False)
async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot))