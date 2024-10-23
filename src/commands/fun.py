import discord, psutil, time, os, aiohttp
from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.bot.version = os.getenv("version")
        
    @discord.slash_command(description="Is IDU deleted?")
    async def idu(self, ctx):
        if (self.bot.get_guild(746844357205950606)):
            await ctx.send("IDU is not deleted.")
        else:
            await ctx.send("IDU is deleted.")
    
    @discord.slash_command(description="Generate freaky text")
    async def freaky(self, ctx: discord.ApplicationContext, *, text: str):
        mapping = {
            "a": "𝓪", "b": "𝓫", "c": "𝓬", "d": "𝓭", "e": "𝓮", "f": "𝓯", "g": "𝓰", "h": "𝓱", "i": "𝓲", "j": "𝓳",
            "k": "𝓴", "l": "𝓵", "m": "𝓶", "n": "𝓷", "o": "𝓸", "p": "𝓹", "q": "𝓺", "r": "𝓻", "s": "𝓼", "t": "𝓽",
            "u": "𝓾", "v": "𝓿", "w": "𝔀", "x": "𝔁", "y": "𝔂", "z": "𝔃", "A": "𝓐", "B": "𝓑", "C": "𝓒", "D": "𝓓",
            "E": "𝓔", "F": "𝓕", "G": "𝓖", "H": "𝓗", "I": "𝓘", "J": "𝓙", "K": "𝓚", "L": "𝓛", "M": "𝓜", "N": "𝓝",
            "O": "𝓞", "P": "𝓟", "Q": "𝓠", "R": "𝓡", "S": "𝓢", "T": "𝓣", "U": "𝓤", "V": "𝓥", "W": "𝓦", "X": "𝓧",
            "Y": "𝓨", "Z": "𝓩"
        }
        result = ""
        for char in text:
            if char in mapping:
                result += mapping[char]
            else:
                result += char
        await ctx.respond(result)
        
    @discord.slash_command(description="Prompt Kendale")
    async def kendale(self, ctx:discord.ApplicationContext, query: str):
        
        await ctx.defer()
        
        ollama_url = "http://localhost:11434/api/generate"
        
        payload = {
            "model": "llama3.1",
            "prompt": query,
            "stream": False
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(ollama_url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    response_text = data.get('response', 'No response from Ollama.')
                    await ctx.respond(response_text)
                
                else:
                    await ctx.respond(f"An error occurred. {response.status}")
        
    
def setup(bot):
    bot.add_cog(Fun(bot))

