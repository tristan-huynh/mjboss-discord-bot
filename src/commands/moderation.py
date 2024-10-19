import discord, psutil, time, os
from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.bot.version = os.getenv("version")
    
    lockdown = SlashCommandGroup("lockdown", "Commands for locking down the server")
    unlock = SlashCommandGroup("unlock", "Commands for unlocking the server")
    purge = SlashCommandGroup("purge", "Commands for purging messages")
    
    @lockdown.command(description="Lockdown a channel")
    async def channel(self, ctx: discord.ApplicationContext):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.respond("Channel has been locked down.")

    @lockdown.command(description="Lockdown server")
    async def server(self, ctx: discord.ApplicationContext):
        for channel in ctx.guild.channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.respond("All channels have been locked down.")
    
    
    @unlock.command(description="Unlock a channel")
    async def channel(self, ctx: discord.ApplicationContext):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.respond("Channel has been unlocked.")
    
    @unlock.command(description="Unlock server")
    async def server(self, ctx: discord.ApplicationContext):
        for channel in ctx.guild.channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.respond("All channels have been unlocked.")
    
    @discord.slash_command(description="Change a users nickname")
    async def forcenickname(self, ctx: discord.ApplicationContext, member: discord.Member, *, nickname: str):
        await member.edit(nick=nickname)
        await ctx.respond(f"Nickname for {member.mention} has been changed to {nickname}.", ephemeral=True)
        
    @discord.slash_command(description="Self destruct the bot")
    async def selfdestruct(self, ctx: discord.ApplicationContext):
        if ctx.author.guild_permissions.administrator:
            await ctx.respond(f"Bye bye! :wave:")
            await ctx.guild.leave()
        else:
            await ctx.respond("You do not have administrative rights.")

        
    @purge.command(description="Purge messages from a channel")
    async def channel(self, ctx: discord.ApplicationContext, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.respond(f"{limit} messages have been purged.")
        
    @purge.command(description="Purge all messages from a user")
    async def user(self, ctx: discord.ApplicationContext, user: discord.User, limit: int):
        # def check(message):
        #     return message.author == user
        
        # Modify so it deletses in chronological order
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.purge(limit=limit, check=lambda message: message.author == user)
        await ctx.respond(f"{limit} messages from {user.mention} have been purged.")
        
    # @discord.slash_command(description="Show a moderators statistics")
    # async def modstat(self, ctx: discord.ApplicationContext, user: discord.User):
        
                
    
def setup(bot):
    bot.add_cog(Moderation(bot))