# IMPORTS
# discord
import discord
from discord.ext import commands
# credentials reading
import yaml


# BOT CONFIG
bot = commands.Bot(command_prefix = "m!", intents = discord.Intents.all())
with open(".secrets.yml") as file:
    secrets = yaml.load(file, Loader = yaml.FullLoader)

bot.run(secrets["bot_token"])