# bot.py
import os
import discord
from dotenv import load_dotenv
import cog

#1
from discord.ext import commands

#get server token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


bot = commands.Bot(command_prefix= '!',description = 'D&D Bot')

# On ready event
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#------------- add cog -------------
bot.add_cog(cog.Greetings(bot))
bot.add_cog(cog.rollDice(bot))
bot.add_cog(cog.character(bot))

bot.run(TOKEN)