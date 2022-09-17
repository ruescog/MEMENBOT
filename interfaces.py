import discord
from textblob import TextBlob
from typing import Optional

class TranslateInterface(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180):
        super().__init__(timeout = timeout)
        self.used = False

    @discord.ui.button(label = "Translate", style = discord.ButtonStyle.blurple, emoji = '🇺🇸')
    async def english(self, interaction: discord.Interaction, button: discord.ui.Button):
        "Toggle to english the language of the message sent."
        if not self.used:
            blob = TextBlob(interaction.message.content)
            response = str(blob.translate(from_lang = "es", to = "en"))
            await interaction.response.edit_message(content = response)
            self.used = True