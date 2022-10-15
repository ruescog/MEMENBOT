import discord
from textblob import TextBlob

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