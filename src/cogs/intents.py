from discord.ext import commands
from discord import app_commands
from io import BytesIO
import discord, re, requests, logging, dotenv, random

import instaloader, praw

class ReactionListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.collection = bot.db["listeners"]
    def blacklist_check():
        async def predicate(interaction: discord.Interaction) -> bool:
            if str(interaction.user.id) in interaction.client.blacklisted_users:
                raise app_commands.CheckFailure("You are currently restricted from accessing this system's commands. Command usage may be monitored to detect unauthorized activity. Unauthorized attempts to access, obtain, upload, modify, change, and/or delete information on this system are strictly prohibited and are subject to criminal prosecution under 18 U.S.C. § 1030, and other applicable statutes, which may result in fines and imprisonment.\n\nThis event has been recorded. If you believe this restriction is in error or wish to appeal, please contact the system administrator.")
            return True
        return app_commands.check(predicate)
    
    async def set_listener(self, guild_id: int, enabled: bool):
        """Set the listener enabled status for a guild."""
        await self.collection.update_one(
            {"guild_id": str(guild_id)},
            {"$set": {"enabled": enabled}},
            upsert=True
        )

    async def clear_listener(self, guild_id: int):
        """Clear the listener setting for a guild."""
        await self.collection.delete_one({"guild_id": str(guild_id)})

    async def get_listener(self, guild_id: int):
        """Get the listener enabled status for a guild."""
        doc = await self.collection.find_one({"guild_id": str(guild_id)})
        return doc.get("enabled", False) if doc else False

    @app_commands.command(name="togglelistener", description="Toggle the reaction listener for this server")
    @blacklist_check()
    async def toggle_listener(self, interaction: discord.Interaction):
        if not interaction.guild:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=False)
            return
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to manage listeners.", ephemeral=False)
            return

        guild_id = interaction.guild.id
        current = await self.get_listener(guild_id)
        new_value = not current
        await self.set_listener(guild_id, new_value)

        await interaction.response.send_message(
            f"Reaction listener is now {'enabled' if new_value else 'disabled'} for this server.",
            ephemeral=False
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        if (str(message.author.id) in self.bot.blacklisted_users):
            return
        if not message.guild or message.author.bot:
            return

        enabled = await self.get_listener(message.guild.id)
        if not enabled:
            return
        
        if "v/s" in message.content.lower():
            await message.add_reaction("⬅️")
            await message.add_reaction("➡️")
        if "y/n" in message.content.lower():
            await message.add_reaction("👍")
            await message.add_reaction("👎")
        
        # if self.bot.user in message.mentions:
        #     await message.channel.send("Hi! 👋")

        if self.bot.user in message.mentions:
            # Extract an Instagram reel URL using regex
            instagram_match = re.search(r"(https?://(?:www\.)?instagram\.com/(?:reel[s]?|p)/[^/\s]+/?)", message.content)
            twitter_match = re.search(r"(https?://(?:www\.)?twitter\.com/[^/\s]+/status/[^/\s]+)", message.content)
            reddit_match = re.search(r"(https?://(?:www\.)?reddit\.com/r/[^/\s]+/comments/[^/\s]+)", message.content)
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 
                'Mozilla/5.0 (X11; U; Linux i586; en-US; rv:1.7.3) Gecko/20040924Epiphany/1.4.4 (Ubuntu)' 
            ]

            if instagram_match:
                reel_url = instagram_match.group(1)
                try:
                    loader = instaloader.Instaloader()
                    
                    loader.context.user_agent = random.choice(user_agents)
                    # loader.context._session.cookies.set(
                    #     name="sessionid",
                    #     value=dotenv.get_key(dotenv.find_dotenv(), "instagram_sessionid"),
                    #     domain=".instagram.com",
                    #     path="/",
                    # )
                    # Extract the shortcode from the URL
                    shortcode = reel_url.rstrip("/").split("/")[-1]
                    logging.info(f"Instagram: Shortcode: {shortcode}")
                    post = instaloader.Post.from_shortcode(loader.context, shortcode)
                    
                    metadata = {
                        "shortcode": post.shortcode,
                        "owner_username": post.owner_username,
                        "caption": post.caption,
                        "video_url": post.video_url if post.is_video else None,
                        "image_url": post.url if not post.is_video else None,
                        "likes": post.likes,
                        "comments": post.comments,
                        "timestamp": post.date_utc.strftime("%Y-%m-%d %H:%M:%S"),
                        "owner_profile_pic": post.owner_profile.profile_pic_url,
                    }
                    logging.debug(f"Instagram: Metadata: {metadata}")
                    if post.is_video:
                        media_url = post.video_url
                        logging.debug(f"Instagram: Media_URL: {media_url}")
                    
                    else:
                        media_url = post.url
                        logging.debug(f"Instagram: Media_URL: {media_url}")


                    # Build an embed linking to the original reel
                    caption = metadata['caption'] if metadata['caption'] else "No caption available."
                    if len(caption) > 100:
                        caption = caption[:100] + "..."
                    embed = discord.Embed(title=caption, url=reel_url, color=self.bot.embed_color)
                    embed.set_author(name=f"{metadata['owner_username']} • 💔 {metadata['likes']} • 💬 {metadata['comments']}", icon_url=metadata["owner_profile_pic"])
                    embed.timestamp = post.date_utc
                    embed.set_footer(
                        icon_url=message.author.avatar.url,
                        text=f"Requested by {message.author.name}"
                    )
                    await message.channel.send(embed=embed, file=discord.File(BytesIO(requests.get(media_url).content), filename="reel.mp4"))
                    # Delete the original message and send the file with embed
                    await message.delete()
                except Exception as e:
                    await message.channel.send(f"Failed to process the Instagram link. Error: {e}")
                    logging.error(f"Error processing Instagram link: {e}")
            elif reddit_match:
                reddit_url = reddit_match.group(1)
                reddit_subreddit = reddit_url.split("/")[-3]
                reddit_post_id = reddit_url.split("/")[-1]
                reddit = praw.Reddit(
                    client_id=dotenv.get_key(dotenv.find_dotenv(), "reddit_client_id"),
                    client_secret=dotenv.get_key(dotenv.find_dotenv(), "reddit_client_secret"),
                    user_agent=dotenv.get_key(dotenv.find_dotenv(), "reddit_user_agent"),
                    check_for_async=False
                )
                logging.debug(f"Reddit: PostID: {reddit_post_id}")
                
                submission = reddit.submission(id=reddit_post_id)
                
                # If the post is a self-post then there's no downloadable media
                if submission.is_self:
                    return
                
                if submission.over_18 and not message.channel.is_nsfw():
                    await message.channel.send("This Reddit post is NSFW and cannot be processed in a non-NSFW channel.")
                    return
                
                # Determine if the submission is an image or video
                file_obj = None
                if hasattr(submission, "post_hint") and submission.post_hint == "image":
                    media_url = submission.url
                    file_extension = media_url.split(".")[-1]
                    file_name = f"{reddit_post_id}.{file_extension}"
                    r = requests.get(media_url)
                    if r.status_code != 200:
                        await message.channel.send("Failed to fetch the Reddit image.")
                        return
                    file_obj = BytesIO(r.content)
                    file_obj.name = file_name
                elif submission.is_video:
                    # For video posts, use the fallback URL in the reddit_video info
                    try:
                        media_url = submission.media["reddit_video"]["fallback_url"]
                        file_name = f"{reddit_post_id}.mp4"
                        r = requests.get(media_url)
                        if r.status_code != 200:
                            await message.channel.send("Failed to fetch the Reddit video.")
                            return
                        file_obj = BytesIO(r.content)
                        file_obj.name = file_name
                    except (KeyError, TypeError):
                        await message.channel.send("No downloadable video found for this Reddit post.")
                        return
                else:
                    await message.channel.send("Reddit post does not contain downloadable media.")
                    return

                # Build an embed that links to the original Reddit post
                embed = discord.Embed(title=submission.title, url=reddit_url, color=self.bot.embed_color)
                embed.set_author(
                    name=f"r/{submission.subreddit.display_name} • {submission.author.name} • 👍 {submission.score} • 💬 {submission.num_comments}",
                    icon_url=submission.author.icon_img
                )
                embed.timestamp = discord.utils.utcnow()
                embed.set_footer(icon_url=message.author.avatar.url if message.author.avatar else None,
                                text=f"Requested by {message.author.name}")

                # Delete the original message and send the file with embed
                await message.delete()
                await message.channel.send(embed=embed, file=discord.File(file_obj, filename=file_obj.name))
            elif twitter_match:
                user, tweet_id = twitter_match.group(1).split("/status/")
                user = user.split("twitter.com/")[-1]
                logging.debug(f"Twitter: User: {user}, TweetID: {tweet_id}")
                
                try:
                    tweet_url = f"https://fxtwitter.com/{user}/status/{tweet_id}"

                    await message.delete()
                    await message.channel.send(tweet_url)
                except Exception as e:
                    await message.channel.send(f"Failed to process the Twitter link. Error: {e}")
            else:
                await message.channel.send("Hi! 👋")
    @toggle_listener.error
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
    await bot.add_cog(ReactionListener(bot))