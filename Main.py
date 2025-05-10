import discord
from discord.ext import commands
from discord.ui import Button, View, Select, SelectOption
from dotenv import load_dotenv
import os

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Hole den Token aus der Umgebungsvariable
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot initialisieren
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Beispiel für eine einfache Zutatenauswahl und Berechnung
# Du kannst hier die Zutaten oder Produkte nach deinem Bedarf anpassen.
products = {
    "Produkt A": {"cost": 100, "price": 200},
    "Produkt B": {"cost": 150, "price": 300},
    "Produkt C": {"cost": 500, "price": 1000},
}

# Funktionsweise der Auswahl
class ProductSelect(Select):
    def __init__(self):
        options = [SelectOption(label=product, value=product) for product in products]
        super().__init__(placeholder="Wähle ein Produkt", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Produktname aus der Auswahl
        product = self.values[0]
        cost = products[product]["cost"]
        price = products[product]["price"]

        # Sende eine Nachricht mit den berechneten Kosten und Preis
        await interaction.response.send_message(
            f"Du hast {product} ausgewählt.\nKosten: {cost}€\nVerkaufspreis: {price}€",
            ephemeral=True,
        )

# !mix Befehl
@bot.command()
async def mix(ctx):
    # Button erstellen
    button = Button(label="Wähle ein Produkt!", style=discord.ButtonStyle.primary)

    # View erstellen und den Button hinzufügen
    view = View()
    view.add_item(button)

    # Wenn der Button geklickt wird, zeige das Dropdown-Menü an
    async def button_callback(interaction: discord.Interaction):
        # Zeige das Dropdown-Menü an, nachdem der Button geklickt wurde
        select = ProductSelect()
        view = View()
        view.add_item(select)
        await interaction.response.send_message("Wähle ein Produkt:", view=view)

    button.callback = button_callback

    # Sende eine Nachricht mit dem Button
    await ctx.send("Klicke den Button, um ein Produkt auszuwählen:", view=view)


# Bot bereit
@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")

# Starte den Bot mit dem Token
bot.run(TOKEN)
