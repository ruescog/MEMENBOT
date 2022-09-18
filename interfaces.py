import discord
from textblob import TextBlob
import utils

class TranslateInterface(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label = "Translate", style = discord.ButtonStyle.blurple, emoji = '🇺🇸')
    async def translation(self, interaction: discord.Interaction, button: discord.ui.Button):
        "Toggle to english the language of the message sent."
        blob: TextBlob = TextBlob(interaction.message.content)
        response: str = str(blob.translate(from_lang = "es", to = "en"))
        thread: discord.Thread = await interaction.message.create_thread(
            name = "translated-message",
            auto_archive_duration = 60
        )
        await thread.add_user(interaction.user)
        await thread.send(content = response)


class RaceSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            options = [discord.SelectOption(label = race) for race in utils.races()],
            placeholder = "Halflings"
        )

    async def callback(self, interaction: discord.Interaction):
        pass


class TeamNameTextInput(discord.ui.TextInput):
    def __init__(self):
        super().__init__(
            label = "Nombre del equipo",
            placeholder = "Pick up & Inscribe",
            default = "Halflings"
        )

    async def callback(self, interaction: discord.Interaction):
        pass

class LeagueInterface(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
        self.add_item(RaceSelect())
        self.add_item(TeamNameTextInput())

    @discord.ui.button(label = "Enviar inscripción", style = discord.ButtonStyle.red, row = 3)
    async def send(self, interaction: discord.Interaction):
        "Defines the select that allow the user to select a race."
        pass