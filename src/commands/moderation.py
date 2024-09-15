import discord
from discord.ext import commands
import psutil
import time


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.bot.version = "1.0.0"

    @discord.slash_command(description="Lockdown a channel")
    async def channel(self, ctx: discord.ApplicationContext):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("Channel has been locked down.")
        
    @discord.slash_command(description="Lockdown server")
    async def server(self, ctx: discord.ApplicationContext):
        for channel in ctx.guild.channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("All channels have been locked down.")
    
    @discord.slash_command(description="Unlock a channel")
    async def unlock(self, ctx: discord.ApplicationContext):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("Channel has been unlocked.")
    
    @discord.slash_command(description="Unlock server")
    async def server(self, ctx: discord.ApplicationContext):
        for channel in ctx.guild.channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("All channels have been unlocked.")

    @discord.slash_command(description="Change a users nickname")
    async def forcenickname(self, ctx: discord.ApplicationContext, member: discord.Member, *, nickname: str):
        await member.edit(nick=nickname)
        await ctx.send(f"Nickname for {member.mention} has been changed to {nickname}.", ephemeral=True)
        
    @discord.slash_command(description="Self destruct the bot")
    async def selfdestruct(self, ctx: discord.ApplicationContext):
        await ctx.guild.leave()
        
    
    @discord.slash_command(description="Specify jail channel")
    async def jailchannel(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        self.bot.jail_channel = channel
        await ctx.send(f"Jail channel has been set to {channel.mention}.")
        
def setup(bot):
    bot.add_cog(Moderation(bot))