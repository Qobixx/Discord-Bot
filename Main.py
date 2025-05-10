import discord
from discord.ext import commands
from discord.ui import Button, View, TextInput, Modal
from dotenv import load_dotenv
import os

# .env laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Modal für Benutzereingabe
class ProductModal(Modal):
    def __init__(self):
        super().__init__(title="Produkt und Zutat Auswahl")
        # Erstelle ein TextInput-Feld für das Produkt
        self.product_input = TextInput(
            label="Produktname",
            placeholder="Gib den Namen des Produkts ein...",
            min_length=1,
            max_length=100,
            required=True
        )
        # Erstelle ein TextInput-Feld für die Zutat
        self.ingredient_input = TextInput(
            label="Zutat",
            placeholder="Gib die Zutat ein...",
            min_length=1,
            max_length=100,
            required=True
        )
        # Füge die TextInputs zu Modal hinzu
        self.add_item(self.product_input)
        self.add_item(self.ingredient_input)

    async def on_submit(self, interaction: discord.Interaction):
        # Holen der Eingabewerte
        product = self.product_input.value
        ingredient = self.ingredient_input.value

        # Simuliere eine Berechnung
        await interaction.response.send_message(
            f"Du hast das Produkt **{product}** und die Zutat **{ingredient}** ausgewählt.\n"
            "Berechne nun die Gesamtkosten und den Gesamtpreis...",
            ephemeral=True
        )

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(f"Es gab einen Fehler: {error}", ephemeral=True)

# !mix Befehl
@bot.command()
async def mix(ctx):
    # Button erstellen
    button = Button(label="Öffne Modal-Fenster!", style=discord.ButtonStyle.primary)

    # View erstellen und den Button hinzufügen
    view = View()
    view.add_item(button)

    # Wenn der Button geklickt wird, öffne das Modal
    async def button_callback(interaction: discord.Interaction):
        modal = ProductModal()
        await interaction.response.send_modal(modal)

    button.callback = button_callback

    # Sende eine Nachricht mit dem Button
    await ctx.send("Klicke auf den Button, um ein Modal-Fenster zu öffnen:", view=view)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
