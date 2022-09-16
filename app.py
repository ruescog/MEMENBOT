# IMPORTS
# discord
from http.client import MOVED_PERMANENTLY
import discord
from discord.ext import commands
# credentials reading
import yaml
# behavior
import wellcome
import utils


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
    view = wellcome.Menu()
    await message.edit(view = view)

# COMMANDS
@bot.command(name = "purge")
@commands.has_role("manager")
async def purge(ctx: commands.Context, n_messages: int = 10):
    "Deletes n_messages messages in the channel that this command is sent."
    if n_messages == -1:
        n_messages = None

    await ctx.channel.purge(limit = n_messages)

@bot.command(name = "manager")
@commands.has_permissions(administrator = True)
async def manager(ctx: commands.Context, member: discord.Member):
    "Grant or revoke the manager role to a member."
    role = await utils.get_role(ctx.guild, "manager")
    if member.get_role(role.id):
        await member.remove_roles(role)
    else:
        await member.add_roles(role)

bot.run(secrets["bot_token"])