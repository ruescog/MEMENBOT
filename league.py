from email import message
import discord

def filter(message: discord.Message):
    "Gets the teamhome and the teamaway from a discord message"
    return {}

def get_elo(data: dict):
    "Gets the elo for each team"
    return data

def calculate_elo(data: dict):
    "Calculates the new elo depending on the match result"
    return data

def save_results(data: dict):
    "Saves the results in the google sheet"
    pass

async def process_message(message: discord.Message):
    data = filter(message)
    data = get_elo(data)
    data = calculate_elo(data)
    save_results(data)