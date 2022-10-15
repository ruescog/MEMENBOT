# IMPORTS
# discord
from typing import Any
import discord
from discord.ext import commands
# credentials reading
import yaml
# behavior
import interfaces
import utils
import league
from textblob import TextBlob


# BOT CONFIG
bot = commands.Bot(command_prefix = "m!", intents = discord.Intents.all())
with open(".secrets.yml") as file:
    secrets = yaml.load(file, Loader = yaml.FullLoader)
with open("settings.yml") as file:    
    settings = yaml.load(file, Loader = yaml.FullLoader)

# EVENT LISTENER
@bot.event
async def on_member_join(member: discord.Member):
    guild: discord.Guild = member.guild
    system_channel: discord.TextChannel = guild.system_channel
    message: str = f"Hola {member.mention}, bienvenido a la comunidad."
    await system_channel.send(message, view = interfaces.TranslateInterface())


@bot.event
async def on_message(message: discord.Message):
    if message.author.id == 782341586188632084: # its me
        return

    if message.content[:2] == "m!":
        await bot.process_commands(message)
    else:
        channel: discord.TextChannel = message.channel

        if channel.id == int(settings["league_results_channel"]):
            league.process_message(message)


# COMMANDS
@bot.command(name = "category_delete")
@commands.has_role("manager")
async def category_delete(ctx: commands.Context):
    "Deletes the category where this command is sent in a recursively way."
    category: discord.CategoryChannel = ctx.channel.category
    for channel in category.channels:
        await channel.delete()

    await category.delete()


@bot.command(name = "config")
@commands.has_role("manager")
async def config(ctx: commands.Context, key: str, value):
    "Sets the channel as the default match reporting channel"
    global settings
    settings = utils.save_settings(settings, key, value)
    await ctx.reply(f"New setting saved: {key} - {value}")


@bot.command(name = "manager")
@commands.has_permissions(administrator = True)
async def manager(ctx: commands.Context, member: discord.Member):
    "Grant or revoke the manager role to a member."
    role: discord.Role = await utils.get_role(ctx.guild, "manager")
    if member.get_role(role.id):
        await member.remove_roles(role)
    else:
        await member.add_roles(role)


@bot.command(name = "purge")
@commands.has_role("manager")
async def purge(ctx: commands.Context, n_messages: int = 10):
    "Deletes n_messages messages in the channel where this command is sent. If n_messages is equal to -1, deletes all the messages."
    if n_messages == -1:
        n_messages = None

    await ctx.channel.purge(limit = n_messages)


@bot.command(name = "translate")
async def translate(ctx: commands.Context, message: str, language_from: str = "es", language_to: str = "en"):
    "Translates a message from a language into another."
    blob: TextBlob = TextBlob(message)
    response: str = str(blob.translate(from_lang = language_from, to = language_to))
    await ctx.reply(response)


bot.run(secrets["bot_token"])