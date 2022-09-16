import discord

def ifnone(*args):
    for arg in args:
        if arg:
            return arg
    
    return None

async def get_role(guild: discord.Guild, role_name: str = None):
    "Gives the role object from a role name."
    role_name = role_name.lower()
    return ifnone(*list(filter(lambda role: role.name.lower() == role_name, guild.roles)))
