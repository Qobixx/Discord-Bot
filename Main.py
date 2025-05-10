import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from dotenv import load_dotenv
import os

# .env laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

produkte = {
    "OgKush": {"cost": 100, "price": 200},
    "Meht": {"cost": 150, "price": 300},
    "Cocain": {"cost": 500, "price": 1000},
}

zutaten = {
    "Gasolin": {"cost": 10, "price": 20},
    "Paper": {"cost": 2, "price": 5},
    "Filter": {"cost": 1, "price": 3},
}

# Funktionsweise der Auswahl für Produkte
class ProduktSelect(Select):
    def __init__(self):
        # Optionen direkt hier definieren
        options = [discord.SelectOption(label=produkt, value=produkt) for produkt in produkte]
        super().__init__(placeholder="Wähle ein Produkt", options=options)

    async def callback(self, interaction: discord.Interaction):
        produkt = self.values[0]
        cost = produkte[produkt]["cost"]
        price = produkte[produkt]["price"]

        # Sende eine Nachricht mit den berechneten Kosten und Preis
        await interaction.response.send_message(
            f"Du hast {produkt} ausgewählt.\nKosten: {cost}€\nVerkaufspreis: {price}€",
            ephemeral=True,
        )

# Funktionsweise der Auswahl für Zutaten
class ZutatSelect(Select):
    def __init__(self):
        # Optionen direkt hier definieren
        options = [discord.SelectOption(label=zutat, value=zutat) for zutat in zutaten]
        super().__init__(placeholder="Wähle eine Zutat", options=options)

    async def callback(self, interaction: discord.Interaction):
        zutat = self.values[0]
        cost = zutaten[zutat]["cost"]
        price = zutaten[zutat]["price"]

        # Sende eine Nachricht mit den berechneten Kosten und Preis
        await interaction.response.send_message(
            f"Du hast {zutat} ausgewählt.\nKosten: {cost}€\nVerkaufspreis: {price}€",
            ephemeral=True,
        )

# !mix Befehl
@bot.command()
async def mix(ctx):
    # Button erstellen
    button = Button(label="Wähle ein Produkt und eine Zutat!", style=discord.ButtonStyle.primary)

    # View erstellen und den Button hinzufügen
    view = View()
    view.add_item(button)

    # Wenn der Button geklickt wird, zeige die Produkt- und Zutatenauswahl an
    async def button_callback(interaction: discord.Interaction):
        produkt_select = ProduktSelect()
        zutat_select = ZutatSelect()
        
        # Eine neue View für die Auswahl von Produkt und Zutat
        view = View()
        view.add_item(produkt_select)
        view.add_item(zutat_select)
        
        # Zeige die Auswahl
        await interaction.response.send_message("Wähle ein Produkt und eine Zutat:", view=view)

    button.callback = button_callback

    # Sende eine Nachricht mit dem Button
    await ctx.send("Klicke den Button, um ein Produkt und eine Zutat auszuwählen:", view=view)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
