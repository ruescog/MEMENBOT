import discord

def ifnone(*args):
    for arg in args:
        if arg:
            return arg
    
    return None

def races():
    return [
        # "EQUIPO0",
        "Humanos",
        "Enanos",
        "Skaven",
        "Orcos",
        "Hombres lagarto",
        "Goblins",
        "Elfos silvanos",
        "Caos",
        "Elfos Oscuros",
        "No muertos",
        "Halflings",
        "Norse",
        "Amazonas",
        "Elfos pro",
        "Altos elfos",
        "Khemri",
        "Nigromantes",
        "Nurgle",
        "Ogros",
        "Vampiros",
        "Enanos del Caos",
        "Inframundo",
        # "EQUIPO23",
        "Bretonia",
        "Kislev"
    ]

async def get_role(guild: discord.Guild, role_name: str = None):
    "Gives the role object from a role name."
    role_name = role_name.lower()
    return ifnone(*list(filter(lambda role: role.name.lower() == role_name, guild.roles)))
