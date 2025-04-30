import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from dotenv import load_dotenv # type: ignore
import os

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()



# Hole den Token aus der Umgebungsvariable
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents (wichtig für Prefix-Commands & Modals)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="_", intents=intents)

# Feedback-Modal
class FeedbackModal(Modal):
    def __init__(self):
        super().__init__(title="📝 Feedbackbogen")
        self.subject = TextInput(label="Betreff", placeholder="Worum geht's?")
        self.feedback = TextInput(label="Dein Feedback",
                                  style=discord.TextStyle.paragraph,
                                  placeholder="Schreibe hier dein Feedback…")
        self.add_item(self.subject)
        self.add_item(self.feedback)

    async def on_submit(self, interaction: discord.Interaction):
        # 1) Ephemeral-Bestätigung an den Einreicher
        await interaction.response.send_message("Danke für dein Feedback! 👍",
                                                ephemeral=True)

        # 2) Feedback als DM an den Server-Owner senden
        guild = interaction.guild
        owner_id = guild.owner_id  # ermittelt automatisch die Owner-ID
        owner = await bot.fetch_user(owner_id)  # User-Objekt des Owners
        await owner.send(
            f"📥 **Neues Feedback**\n"
            f"• **Von:** {interaction.user} (ID: {interaction.user.id})\n"
            f"• **Rolle:** {interaction.user.top_role.name}\n"          # top_role = höchste Rolle des Users
            f"• **Betreff:** {self.subject.value}\n"
            f"• **Feedback:**\n> {self.feedback.value}")


# Command, der den Feedback-Button ausgibt
@bot.command()
async def feedback(ctx):
    btn = Button(label="Feedback ausfüllen",
                 style=discord.ButtonStyle.primary,
                 custom_id="open_feedback")
    view = View()
    view.add_item(btn)

    async def open_modal(interaction: discord.Interaction):
        await interaction.response.send_modal(FeedbackModal())

    btn.callback = open_modal

    await ctx.send("Klicke auf den Button, um den Feedbackbogen zu öffnen:",
                   view=view)


@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")


bot.run(TOKEN)
