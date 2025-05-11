<<<<<<< HEAD
from discord.ext import commands
from discord import app_commands
import discord, asyncio 


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    def blacklist_check():
        async def predicate(interaction: discord.Interaction) -> bool:
            if str(interaction.user.id) in interaction.client.blacklisted_users:
                raise app_commands.CheckFailure("You are currently restricted from accessing this system's commands. Command usage may be monitored to detect unauthorized activity. Unauthorized attempts to access, obtain, upload, modify, change, and/or delete information on this system are strictly prohibited and are subject to criminal prosecution under 18 U.S.C. § 1030, and other applicable statutes, which may result in fines and imprisonment.\n\nThis event has been recorded. If you believe this restriction is in error or wish to appeal, please contact the system administrator.")
            return True
        return app_commands.check(predicate)
    
    lockdown_group = app_commands.Group(name="lockdown", description="Lockdown commands")
    unlock_group = app_commands.Group(name="unlock", description="Unlock commands")
    purge_group = app_commands.Group(name="purge", description="Purge commands")
    warn_group = app_commands.Group(name="warn", description="Warn commands")
    
    @app_commands.command(name="kick", description="Kick a user from the server")
    @app_commands.describe(member="The member to kick", reason="The reason for kicking the member")
    # @app_commands.checks.has_permissions(kick_members=True)
    @blacklist_check()
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        # await interaction.response.defer(ephemeral=False)
        if not interaction.user.guild_permissions.kick_members:
             await interaction.response.send_message("You do not have permission to kick members.", ephemeral=False)
             return
        if reason is None:
            reason = "No reason provided"
        try:
            await member.send(f"You have been kicked from {interaction.guild.name} for: {reason}")
            await member.kick(reason=reason)

        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"{member.mention} has been kicked for: {reason}", ephemeral=False)
    
    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.describe(member="The member to ban", reason="The reason for the ban")
    # @app_commands.checks.has_permissions(ban_members=True)
    @blacklist_check()
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        # await interaction.response.defer(ephemeral=False)
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("You do not have permission to ban members.", ephemeral=False)
            return
        if reason is None:
            reason = "No reason provided"
        try:
            await member.send(f"You have been banned from {interaction.guild.name} for: {reason}")
            await member.ban(reason=reason, delete_message_seconds=604800)
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"{member.mention} has been banned for: {reason}", ephemeral=False)
    
    @lockdown_group.command(name="channel", description="Lock down a channel")
    @app_commands.describe(channel="The channel to lock down", reason="The reason for the lockdown")
    # @app_commands.checks.has_permissions(manage_channels=True)
    @blacklist_check()    
    async def lockdown_channel(self, interaction: discord.Interaction, channel: discord.TextChannel = None, reason: str = None):
        # await interaction.response.defer(ephemeral=False)
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You do not have permission to manage channels.", ephemeral=False)
            return
        if channel is None:
            channel = interaction.channel
        if reason is None:
            reason = "No reason provided"
        try:
            await channel.set_permissions(interaction.guild.default_role, send_messages=False, reason=reason)
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"{channel.mention} has been locked down for: {reason}", ephemeral=False)

    @lockdown_group.command(name="server", description="Lock down the server")
    @app_commands.describe(reason="The reason for the lockdown")
    # @app_commands.checks.has_permissions(manage_channels=True)
    @blacklist_check()
    async def lockdown_server(self, interaction: discord.Interaction, reason: str = None):
        # await interaction.response.defer(ephemeral=False)
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You do not have permission to manage channels.", ephemeral=False)
            return
        if reason is None:
            reason = "No reason provided"
        try:
            for channel in interaction.guild.text_channels:
                await channel.set_permissions(interaction.guild.default_role, send_messages=False, reason=reason)
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"The server has been locked down for: {reason}", ephemeral=False)
    
    @unlock_group.command(name="channel", description="Unlock a channel")
    @app_commands.describe(channel="The channel to unlock", reason="The reason for the unlock")
    # @app_commands.checks.has_permissions(manage_channels=True)
    @blacklist_check()
    async def unlock_channel(self, interaction: discord.Interaction, channel: discord.TextChannel = None, reason: str = None):
        # await interaction.response.defer(ephemeral=False)
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You do not have permission to manage channels.", ephemeral=False)
            return
        if channel is None:
            channel = interaction.channel
        if reason is None:
            reason = "No reason provided"
        try:
            await channel.set_permissions(interaction.guild.default_role, send_messages=True, reason=reason)
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"{channel.mention} has been unlocked for: {reason}", ephemeral=False)
        
    @unlock_group.command(name="server", description="Unlock the server")
    @app_commands.describe(reason="The reason for the unlock")
    @blacklist_check()
    async def unlock_server(self, interaction: discord.Interaction, reason: str = None):
        # await interaction.response.defer(ephemeral=False)
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You do not have permission to manage channels.", ephemeral=False)
            return
        if reason is None:
            reason = "No reason provided"
        try:
            for channel in interaction.guild.text_channels:
                await channel.set_permissions(interaction.guild.default_role, send_messages=True, reason=reason)
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"The server has been unlocked for: {reason}", ephemeral=False)
    
    @app_commands.command(name="kendale", description="Kendale")
    @blacklist_check()
    async def kendale(self, interaction: discord.Interaction):
        # if not interaction.user.guild_permissions.administrator:
        #     await interaction.response.send_message("You do not have permission to use this command.", ephemeral=False)
        #     return
        await interaction.response.send_message("Hi! 👋", ephemeral=False)
    
    @purge_group.command(name="channel", description="Purge messages from a channel")
    @app_commands.describe(amount="The number of messages to purge")
    @blacklist_check()
    async def purge_channel(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You do not have permission to manage messages.", ephemeral=False)
            return
        if amount < 1 or amount > 100:
            await interaction.response.send_message("Please enter a number between 1 and 100.", ephemeral=False)
            return
        deleted = await interaction.channel.purge(limit=amount + 1)
        await interaction.send(f"Purged {len(deleted) - 1} messages.", ephemeral=False)
    
    @purge_group.command(name="user", description="Purge messages from a user")
    @app_commands.describe(member="The member to purge", amount="The number of messages to purge")
    @blacklist_check()
    async def purge_user(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You do not have permission to manage messages.", ephemeral=False)
            return
        if amount < 1 or amount > 100:
            await interaction.response.send_message("Please enter a number between 1 and 100.", ephemeral=False)
            return
        await interaction.response.defer(ephemeral=False)
        total_deleted = 0
        # Iterate over all text channels in the guild.
        for channel in interaction.guild.text_channels:
            try:
                # Purge messages where the author matches the specified member.
                deleted = await channel.purge(limit=amount, check=lambda m: m.author.id == member.id)
                total_deleted += len(deleted)
                await asyncio.sleep(1)  # small delay to avoid rate limits
            except discord.Forbidden:
                continue  # skip channels where the bot lacks permission

        await interaction.followup.send(f"Purged a total of {total_deleted} messages from all channels.", ephemeral=False)
    
    @purge_group.command(name="message", description="Purge messages from a specific message")
    @app_commands.describe(message_id="The message to purge from", amount="The number of messages to purge")
    @blacklist_check()
    async def purge_from_message(self, interaction: discord.Interaction, message_id: str, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You do not have permission to manage messages.", ephemeral=False)
            return
        if amount < 1 or amount > 100:
            await interaction.response.send_message("Please enter a number between 1 and 100.", ephemeral=False)
            return
        await interaction.response.defer(ephemeral=False)
        
        try:
            message_id = int(message_id) 
            message = await interaction.channel.fetch_message(message_id)
        except discord.NotFound:
            await interaction.followup.send("Message not found.", ephemeral=False)
            return
        deleted = await interaction.channel.purge(limit=amount + 1, after=message.created_at)
        await interaction.followup.send(f"Purged {len(deleted) - 1} messages.", ephemeral=False)

    @app_commands.command(name="nickname", description="Change a user's nickname")
    @app_commands.describe(member="The member to change the nickname for", nickname="The new nickname")
    @blacklist_check()
    async def nickname(self, interaction: discord.Interaction, member: discord.Member, nickname: str):
        if not interaction.user.guild_permissions.manage_nicknames:
            await interaction.response.send_message("You do not have permission to manage nicknames.", ephemeral=False)
            return
        try:
            await member.edit(nick=nickname)
            await interaction.response.send_message(f"Changed {member.mention}'s nickname to {nickname}", ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to change nicknames.", ephemeral=False)
    
    @warn_group.command(name="user", description="Warn a user")
    @app_commands.describe(member="The member to warn", reason="The reason for the warning")
    @blacklist_check()
    async def warn_user(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("You do not have permission to warn members.", ephemeral=False)
            return
        if reason is None:
            reason = "No reason provided"
        try:
            await member.send(f"You have been warned in {interaction.guild.name} for: {reason}")
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"{member.mention} has been warned for: {reason}", ephemeral=False)
    
    @warn_group.command(name="show", description="Show the warnings for a user")
    @app_commands.describe(member="The member to show warnings for")
    @blacklist_check()
    async def show_warnings(self, interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("You do not have permission to view warnings.", ephemeral=False)
            return
        # Fetch warnings from the database (not implemented in this example)
        # For demonstration, we'll use a placeholder message.
        warnings = "No warnings found."  # Replace with actual warning retrieval logic
        await interaction.response.send_message(f"Warnings for {member.mention}: {warnings}", ephemeral=False)
    
    @show_warnings.error
    @warn_user.error
    @nickname.error
    @purge_user.error
    @purge_channel.error
    @purge_from_message.error
    @kendale.error    
    @unlock_channel.error
    @unlock_server.error
    @lockdown_channel.error
    @lockdown_server.error
    @kick.error
    @ban.error
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
=======
from discord.ext import commands
from discord import app_commands
import discord, asyncio 


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def blacklist_check():
        async def predicate(interaction: discord.Interaction) -> bool:
            if str(interaction.user.id) in interaction.client.blacklisted_users:
                raise app_commands.CheckFailure("You are currently restricted from accessing this system's commands. Command usage may be monitored to detect unauthorized activity. Unauthorized attempts to access, obtain, upload, modify, change, and/or delete information on this system are strictly prohibited and are subject to criminal prosecution under 18 U.S.C. § 1030, and other applicable statutes, which may result in fines and imprisonment.\n\nThis event has been recorded. If you believe this restriction is in error or wish to appeal, please contact the system administrator.")
            return True
        return app_commands.check(predicate)
    
    @app_commands.command(name="kick", description="Kick a user from the server")
    @app_commands.describe(member="The member to kick", reason="The reason for kicking the member")
    # @app_commands.checks.has_permissions(kick_members=True)
    @blacklist_check()
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        # await interaction.response.defer(ephemeral=False)
        if not interaction.user.guild_permissions.kick_members:
             await interaction.response.send_message("You do not have permission to kick members.", ephemeral=False)
             return
        if reason is None:
            reason = "No reason provided"
        try:
            await member.send(f"You have been kicked from {interaction.guild.name} for: {reason}")
            await member.kick(reason=reason)

        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"{member.mention} has been kicked for: {reason}", ephemeral=False)
    
    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.describe(member="The member to ban", reason="The reason for the ban")
    # @app_commands.checks.has_permissions(ban_members=True)
    @blacklist_check()
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        # await interaction.response.defer(ephemeral=False)
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("You do not have permission to ban members.", ephemeral=False)
            return
        if reason is None:
            reason = "No reason provided"
        try:
            await member.send(f"You have been banned from {interaction.guild.name} for: {reason}")
            await member.ban(reason=reason, delete_message_seconds=604800)
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"{member.mention} has been banned for: {reason}", ephemeral=False)
    
    @app_commands.command(name="lockdown", description="Lock down a channel")
    @app_commands.describe(channel="The channel to lock down", reason="The reason for the lockdown")
    # @app_commands.checks.has_permissions(manage_channels=True)
    @blacklist_check()    
    async def lockdown(self, interaction: discord.Interaction, channel: discord.TextChannel = None, reason: str = None):
        # await interaction.response.defer(ephemeral=False)
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You do not have permission to manage channels.", ephemeral=False)
            return
        if channel is None:
            channel = interaction.channel
        if reason is None:
            reason = "No reason provided"
        try:
            await channel.set_permissions(interaction.guild.default_role, send_messages=False, reason=reason)
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"{channel.mention} has been locked down for: {reason}", ephemeral=False)

    @app_commands.command(name="unlock", description="Unlock a channel")
    @app_commands.describe(channel="The channel to unlock", reason="The reason for the unlock")
    # @app_commands.checks.has_permissions(manage_channels=True)
    @blacklist_check()
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None, reason: str = None):
        # await interaction.response.defer(ephemeral=False)
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You do not have permission to manage channels.", ephemeral=False)
            return
        if channel is None:
            channel = interaction.channel
        if reason is None:
            reason = "No reason provided"
        try:
            await channel.set_permissions(interaction.guild.default_role, send_messages=True, reason=reason)
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"{channel.mention} has been unlocked for: {reason}", ephemeral=False)
        
    @app_commands.command(name="kendale", description="Kendale")
    @blacklist_check()
    async def kendale(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=False)
            return
        await interaction.response.send_message("Kent", ephemeral=False)
    
    @app_commands.command(name="purge_channel", description="Purge messages from a channel")
    @app_commands.describe(amount="The number of messages to purge")
    async def purge_channel(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You do not have permission to manage messages.", ephemeral=False)
            return
        if amount < 1 or amount > 100:
            await interaction.response.send_message("Please enter a number between 1 and 100.", ephemeral=False)
            return
        await interaction.response.defer(ephemeral=False)
        deleted = await interaction.channel.purge(limit=amount + 1)
        await interaction.followup.send(f"Purged {len(deleted) - 1} messages.", ephemeral=False)
    
    @app_commands.command(name="purge_user", description="Purge messages from a user")
    @app_commands.describe(member="The member to purge", amount="The number of messages to purge")
    async def purge_user(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You do not have permission to manage messages.", ephemeral=False)
            return
        if amount < 1 or amount > 100:
            await interaction.response.send_message("Please enter a number between 1 and 100.", ephemeral=False)
            return
        await interaction.response.defer(ephemeral=False)
        total_deleted = 0
        # Iterate over all text channels in the guild.
        for channel in interaction.guild.text_channels:
            try:
                # Purge messages where the author matches the specified member.
                deleted = await channel.purge(limit=amount, check=lambda m: m.author.id == member.id)
                total_deleted += len(deleted)
                await asyncio.sleep(1)  # small delay to avoid rate limits
            except discord.Forbidden:
                continue  # skip channels where the bot lacks permission

        await interaction.followup.send(f"Purged a total of {total_deleted} messages from all channels.", ephemeral=False)
        
    @purge_user.error
    @purge_channel.error
    @kendale.error    
    @unlock.error
    @lockdown.error
    @kick.error
    @ban.error
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
>>>>>>> 5d5dcf713c0cba9662de2458477d13a741d7f3dd
    await bot.add_cog(Moderation(bot))