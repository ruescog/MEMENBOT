import discord

import googleconnection
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

LIGA_SHEET: str = "1DJeDrP9O79FyyuYqglmqUJ-q-eDHStyr9aJVzvcugB8"
PLAYERS_RANGE: str = "_Jugadores!A1:F100"

def get_info(message: discord.Message):
    "Gets the teamhome and the teamaway from a discord message"
    if not message.embeds:
        return None, None, None, None

    match_info: str = message.embeds[0].title

    if " vs " not in match_info:
        return None, None, None, None
    
    teams: list = match_info.split(" vs ")
    teamhome: str = teams[0]
    teamaway: str = teams[1]

    match_info = message.embeds[0].fields[0].value.split("\n")[1].split(" ")
    index: int = 1
    while index < len(match_info):
        if match_info[index]:
            tdhome: int = int(match_info[index])
            break

        index += 1

    index += 1    
    while index < len(match_info):
        if match_info[index]:
            tdaway: int = int(match_info[index])
            break

        index += 1

    return teamhome, teamaway, tdhome, tdaway

def get_elo(teamhome: str, teamaway: str):
    "Gets the elo for each team"
    creds: Credentials = googleconnection.get_creds()

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    response = sheet.values().get(
        spreadsheetId = LIGA_SHEET,
        range = PLAYERS_RANGE
    ).execute().get("values", [])

    _teamhome = list(filter(lambda row: row[1][2] == teamhome, enumerate(response)))[:1]
    _teamaway = list(filter(lambda row: row[1][2] == teamaway, enumerate(response)))[:1]
    filtered_response = _teamhome + _teamaway
    if len(filtered_response) != 2:
        raise Exception(f"Not enough teams in match {teamhome} vs {teamaway}.\n{filtered_response}")

    return list(map(lambda row: [row[0] + 1, float(row[1][4].replace(",", "."))], filtered_response))

def calculate_elo(elohome: float, eloaway: float, tdhome: int, tdaway: int):
    "Calculates the new elo depending on the match result"
    GIVENELO = 12

    fphome = elohome / (elohome + eloaway)
    fpaway = eloaway / (elohome + eloaway)
    givenhome = fphome * GIVENELO
    givenaway = fpaway * GIVENELO
    elohome -= givenhome
    eloaway -= givenaway

    # Realizar el cambio de ELO
    if tdhome > tdaway:
        elohome += GIVENELO
    elif tdaway > tdhome:
        eloaway += GIVENELO
    else:
        elohome += GIVENELO / 2
        eloaway += GIVENELO / 2

    return round(elohome, 4), round(eloaway, 4)

def save_results(indexhome: int, indexaway: int, elohome: float, eloaway: float):
    "Saves the results in the google sheet"
    creds: Credentials = googleconnection.get_creds()
    range_blueprint: str = "_Jugadores!E#"
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    response = sheet.values().update(
        spreadsheetId = LIGA_SHEET,
        range = range_blueprint.replace("#", str(indexhome)),
        valueInputOption = "USER_ENTERED",
        body = {"values": [[elohome]]}
    ).execute()

    response = sheet.values().update(
        spreadsheetId = LIGA_SHEET,
        range = range_blueprint.replace("#", str(indexaway)),
        valueInputOption = "USER_ENTERED",
        body = {"values": [[eloaway]]}
    ).execute()

def color_range(teamhome: str, teamaway: str):
    "Colour the range in the matches sheet"
    creds: Credentials = googleconnection.get_creds()
    range_blueprint: str = "Ronda actual!A2:G100"
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    response = sheet.values().get(
        spreadsheetId = LIGA_SHEET,
        range = range_blueprint.replace("#", "2", 1).replace("#", "100")
    ).execute().get("values", [])

    row = list(filter(lambda row: row[1][1] in [teamhome, teamaway], enumerate(response)))[:1]

    if row:
        response = sheet.values().update(
            spreadsheetId = LIGA_SHEET,
            range = f"Ronda actual!H{row[0][0] + 2}",
            valueInputOption = "USER_ENTERED",
            body = {"values": [["Sí"]]}
        ).execute()
    else:
        raise Exception(f"No row in the matches sheet found. {teamhome}, {teamaway}")

def process_message(message: discord.Message, save = True):
    teamhome, teamaway, tdhome, tdaway = get_info(message)
    if not teamhome:
        return

    home, away = get_elo(teamhome, teamaway)
    indexhome, elohome = home
    indexaway, eloaway = away
    elohome, eloaway = calculate_elo(elohome, eloaway, tdhome, tdaway)
    if save:
        save_results(indexhome, indexaway, elohome, eloaway)
        color_range(teamaway, teamhome)