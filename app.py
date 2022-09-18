# IMPORTS
# discord
import discord
from discord.ext import commands
# credentials reading
import yaml
# behavior
import interfaces
import utils
from textblob import TextBlob


# BOT CONFIG
bot = commands.Bot(command_prefix = "m!", intents = discord.Intents.all())
with open(".secrets.yml") as file:
    secrets = yaml.load(file, Loader = yaml.FullLoader)

# EVENT LISTENER
@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    system_channel = guild.system_channel
    message = f"Hola {member.mention}, bienvenido a la comunidad."
    message = await system_channel.send(message)
    await message.edit(view = interfaces.TranslateInterface())


# COMMANDS
@bot.command(name = "category_delete")
@commands.has_role("manager")
async def category_delete(ctx: commands.Context):
    "Deletes the category where this command is sent in a recursively way."
    category = ctx.channel.category
    for channel in category.channels:
        await channel.delete()

    await category.delete()


@bot.command(name = "league_new")
@commands.has_role("manager")
async def league_new(ctx: commands.Context, league_name: str):
    "Creates the infraestructure needed to manage a league."
    league_category = await ctx.guild.create_category_channel(league_name)
    league_general = await league_category.create_text_channel("General")
    league_enrolment = await league_category.create_text_channel("Inscripciones")
    league_matches = await league_category.create_text_channel("Partidos")
    league_top = await league_category.create_text_channel("Top")

    message = f"Bienvenidos a la _{league_name}_ liga de Blood Bowl.\n"
    message += f"Para registrarse, consulta la información en {league_enrolment.mention}.\n"
    message += f"También puedes consultar los partidos jugados en {league_matches.mention}.\n"
    message += f"Finalmente, puedes ver el podium en {league_top.mention}."
    message = await league_general.send(message)
    await message.edit(view = interfaces.TranslateInterface())


@bot.command(name = "manager")
@commands.has_permissions(administrator = True)
async def manager(ctx: commands.Context, member: discord.Member):
    "Grant or revoke the manager role to a member."
    role = await utils.get_role(ctx.guild, "manager")
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
    blob = TextBlob(message)
    response = str(blob.translate(from_lang = language_from, to = language_to))
    await ctx.reply(response)


bot.run(secrets["bot_token"])