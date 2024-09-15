import discord
from discord.ext import commands
import psutil
import time


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.bot.version = "1.0.0"
        
    # @discord.slash_command(description="Add an emoji to the server")
    # async def steak(self, ctx: discord.Context, emoji_url: str, emoji_name: str):
    #     try:
    #         response = await self.bot.http.request(
    #             discord.http.Route(
    #                 "POST",
    #                 f"/guilds/{ctx.guild.id}/emojis",
    #             ),
    #             json={
    #                 "name": emoji_name,
    #                 "image": emoji_url,
    #             },
    #         )
    #         emoji = discord.Emoji(guild=ctx.guild, state=self.bot._connection, data=response)
    #         await ctx.send(f"Emoji {emoji} has been added to the server!")
    #     except discord.HTTPException as e:
    #         await ctx.send(f"Failed to add emoji: {e}")
    
    
            
def setup(bot):
    bot.add_cog(Fun(bot))

