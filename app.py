# IMPORTS
# discord
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
with open(".secrets/.secrets.yml") as file:
    secrets = yaml.load(file, Loader = yaml.FullLoader)


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

        if utils.is_league(channel):
            league.process_message(message)

        minutes = utils.volatile(channel)
        if minutes != 0:
            await channel.send(f"{message.author.mention} said:\n" + message.content, delete_after = minutes)
            await message.delete()


@bot.command(name = "category_delete")
@commands.has_role("manager")
async def category_delete(ctx: commands.Context):
    "Deletes the category where this command is sent in a recursively way."
    category: discord.CategoryChannel = ctx.channel.category
    for channel in category.channels:
        await channel.delete()

    await category.delete()


@bot.command(name = "league_results")
@commands.has_role("manager")
async def league_results(ctx: commands.Context, definitive: str = ""):
    "Saves all the league results in the channel"
    channel: discord.TextChannel = await ctx.guild.fetch_channel(utils.load_settings()["channel_league"])
    matches = 0
    async for message in channel.history(oldest_first = True):
        league.process_message(message, save = definitive != "")
        matches += 1

    await ctx.reply(f"League round saved. {int(matches / 3)} matches played.")
    if definitive != "":
        await channel.purge(limit = None)


@bot.command(name = "league_new_round")
@commands.has_role("manager")
async def league_new_round(ctx: commands.Context):
    "Generates a new round"
    round_channel: discord.TextChannel = ctx.channel
    
    # deletes all the information of the round (thread, messages and the name of the channel)
    for thread in round_channel.threads:
        await thread.delete()

    await round_channel.purge(limit = None)

    new_round = int(round_channel.name.split("-")[2]) + 1
    await round_channel.edit(name = f"quedadas-jornada-{new_round}")


@bot.command(name = "channel_volatile")
@commands.has_role("manager")
async def channel_volatile(ctx: commands.Context, minutes: int = 0):
    "Sets the channel as volatile."
    settings = utils.load_settings()
    channel: discord.TextChannel = ctx.channel
    volatile_channels = settings["volatile_channels"]
    volatile_channels.update({
        str(channel.id): minutes
    })

    utils.save_settings("volatile_channels", volatile_channels)
    await ctx.reply(f"{channel.mention} is now a volatile channel.")


@bot.command(name = "channel_league")
@commands.has_role("manager")
async def channel_league(ctx: commands.Context):
    "Sets a channel as the default league channel."
    channel: discord.TextChannel = ctx.channel
    utils.save_settings("channel_league", channel.id)
    await ctx.reply(f"New league channel: {channel.mention}")


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