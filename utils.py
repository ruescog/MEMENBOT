import discord
import json

def ifnone(*args):
    for arg in args:
        if arg:
            return arg
    
    return None

def volatile(channel: discord.TextChannel):
    settings = load_settings()
    for volatile_channel in settings["volatile_channels"]:
        if channel.id == int(volatile_channel):
            return settings["volatile_channels"][volatile_channel] * 60
    
    return 0

def is_league(channel: discord.TextChannel):
    settings = load_settings()
    return channel.id == settings["channel_league"]

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

def load_settings():
    with open("settings.json") as file:    
        return json.load(file)

def save_settings(key: str, value):
    settings = load_settings()
    settings.update({key: value})
    with open("settings.json", "w") as file:    
        json.dump(settings, file)

    return settings