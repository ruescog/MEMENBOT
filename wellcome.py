import discord
from typing import Optional

class Menu(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.value = None

    @discord.ui.button(label = "Send message", style = discord.ButtonStyle.green)
    async def english(self, interaction: discord.Interaction, button: discord.ui.Button):
        "Gives the wellcome in english"
        await interaction.response.edit_message(content = "Hello you clicked me!")