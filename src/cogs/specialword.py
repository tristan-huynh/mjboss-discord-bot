from discord.ext import commands
from discord import app_commands
import discord, string


class SpecialWord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collection = bot.db["specialwords_tracker"]
    def blacklist_check():
        async def predicate(interaction: discord.Interaction) -> bool:
            if str(interaction.user.id) in interaction.client.blacklisted_users:
                raise app_commands.CheckFailure("You are currently restricted from accessing this system's commands. Command usage may be monitored to detect unauthorized activity. Unauthorized attempts to access, obtain, upload, modify, change, and/or delete information on this system are strictly prohibited and are subject to criminal prosecution under 18 U.S.C. § 1030, and other applicable statutes, which may result in fines and imprisonment.\n\nThis event has been recorded. If you believe this restriction is in error or wish to appeal, please contact the system administrator.")
            return True
        return app_commands.check(predicate)
    
    async def increment_word_count(self, user: discord.User):
        user_id = str(user.id)
        username = f"{user.name}#{user.discriminator}"

        await self.collection.update_one(
            {"_id": user_id},
            {"$inc": {"word_count": 1}, "$set": {"username": username}},
            upsert=True
        )

    async def get_leaderboard(self, limit: int = 10):
        cursor = self.collection.find().sort("word_count", -1).limit(limit)
        return await cursor.to_list(length=limit)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        content = message.content.lower()
        banned_words = {"nigger", "nigga", "idu"}
        words = [word.strip(string.punctuation).lower() for word in content.split()]
        if any(word in banned_words or (word.endswith("s") and word[:-1] in banned_words) for word in words):
            await self.increment_word_count(message.author)

    @app_commands.command(name="leaderboard", description="Displays the global leaderboard")
    @blacklist_check()
    async def leaderboard(self, interaction: discord.Interaction):
        leaderboard = await self.get_leaderboard()
        
        if not leaderboard:
            await interaction.response.send_message("No data available for the leaderboard yet.", ephemeral=False)
            return

        embed = discord.Embed(
            title="Global Slur Leaderboard",
            color=self.bot.embed_color,
        )
        embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"{self.bot.user.name} v{self.bot.version}")
        embed.timestamp = discord.utils.utcnow()
        leaderboard_str=""
        for index, entry in enumerate(leaderboard[:10], start=1):
            leaderboard_str += f"{index}. **{entry['username']}** - {entry['word_count']}\n"
        embed.add_field(name="", value=leaderboard_str, inline=False)
        
        # Get current user's word count and rank
        user_id = str(interaction.user.id)
        user_doc = await self.collection.find_one({"_id": user_id})
        user_count = user_doc.get("word_count", 0) if user_doc else 0
        rank = await self.collection.count_documents({"word_count": {"$gt": user_count}}) + 1

        embed.add_field(
            name="Your Rank",
            value=f"Rank #{rank}: **{interaction.user.name}** - {user_count}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
        
    @leaderboard.error
    
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
    await bot.add_cog(SpecialWord(bot))    