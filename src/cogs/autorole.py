from discord.ext import commands
from discord import app_commands
import discord


class Autorole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.collection = bot.db["autoroles"]  
    def blacklist_check():
        async def predicate(interaction: discord.Interaction) -> bool:
            if str(interaction.user.id) in interaction.client.blacklisted_users:
                raise app_commands.CheckFailure("You are currently restricted from accessing this system's commands. Command usage may be monitored to detect unauthorized activity. Unauthorized attempts to access, obtain, upload, modify, change, and/or delete information on this system are strictly prohibited and are subject to criminal prosecution under 18 U.S.C. § 1030, and other applicable statutes, which may result in fines and imprisonment.\n\nThis event has been recorded. If you believe this restriction is in error or wish to appeal, please contact the system administrator.")
            return True
        return app_commands.check(predicate)
    
    autorole_group = app_commands.Group(name="autorole", description="Autorole commands")
    
    async def set_autorole(self, guild_id: int, role_id: int):
        await self.collection.update_one(
            {"guild_id": str(guild_id)},
            {"$set": {"role_id": str(role_id)}},
            upsert=True
        )

    async def clear_autorole(self, guild_id: int):
        await self.collection.delete_one({"guild_id": str(guild_id)})

    async def get_autorole(self, guild_id: int):
        result = await self.collection.find_one({"guild_id": str(guild_id)})
        return result["role_id"] if result else None

    @autorole_group.command(name="set", description="Set a role to be assigned to new members.")
    # @app_commands.default_permissions(manage_roles=True)
    @blacklist_check()
    async def setautorole(self, interaction: discord.Interaction, role: discord.Role):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You do not have permission to manage roles.", ephemeral=False)
            return
            
        guild_id = interaction.guild_id

        if role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "I cannot assign that role. Ensure it is below my highest role.",
                ephemeral=False
            )
            return

        await self.set_autorole(guild_id, role.id)
        await interaction.response.send_message(
            f"Autorole set to {role.mention} for this server.",
            ephemeral=False
        )

    @autorole_group.command(name="clear", description="Clear the autorole setting for this server.")
    # @app_commands.default_permissions(manage_roles=True)
    @blacklist_check()
    async def clearautorole(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You do not have permission to manage roles.", ephemeral=False)
            return
        guild_id = interaction.guild_id
        await self.clear_autorole(guild_id)
        await interaction.response.send_message("Autorole has been cleared for this server.", ephemeral=False)

    @autorole_group.command(name="show", description="Show the current autorole setting for this server.")
    @blacklist_check()
    async def showautorole(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        role_id = await self.get_autorole(guild_id)

        if role_id:
            role = interaction.guild.get_role(int(role_id))
            if role:
                await interaction.response.send_message(
                    f"The current autorole is {role.mention}.",
                    ephemeral=False
                )
            else:
                await interaction.response.send_message(
                    "The autorole is set, but the role no longer exists.",
                    ephemeral=False
                )
        else:
            await interaction.response.send_message("No autorole has been set for this server.", ephemeral=False)
    
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_id = member.guild.id
        role_id = await self.get_autorole(guild_id)

        if role_id:
            role = member.guild.get_role(int(role_id))
            if role:
                try:
                    await member.add_roles(role, reason="Autorole assignment")
                except discord.Forbidden:
                    print(f"Insufficient permissions to assign {role.name} to {member.name}")
    @showautorole.error
    @clearautorole.error
    @setautorole.error
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
    await bot.add_cog(Autorole(bot))    