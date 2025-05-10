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
        self.product = self.values[0]  # Das ausgewählte Produkt speichern
        # Speicher die Auswahl für später
        await interaction.response.send_message(f"Du hast das Produkt **{self.product}** ausgewählt!", ephemeral=True)

# Funktionsweise der Auswahl für Zutaten
class ZutatSelect(Select):
    def __init__(self):
        # Optionen direkt hier definieren
        options = [discord.SelectOption(label=zutat, value=zutat) for zutat in zutaten]
        super().__init__(placeholder="Wähle eine Zutat", options=options)

    async def callback(self, interaction: discord.Interaction):
        self.ingredient = self.values[0]  # Die ausgewählte Zutat speichern
        # Speicher die Auswahl für später
        await interaction.response.send_message(f"Du hast die Zutat **{self.ingredient}** ausgewählt!", ephemeral=True)


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


# Berechnung der Gesamtkosten und des Verkaufspreises
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if isinstance(interaction.data["component_type"], discord.ui.Select):
        # Wenn sowohl Produkt als auch Zutat ausgewählt wurden
        try:
            # Kosten und Preise der ausgewählten Produkte und Zutaten
            product = produkte[interaction.data["product"]]
            ingredient = zutaten[interaction.data["ingredient"]]

            # Berechnung der Gesamtkosten und des Verkaufspreises
            total_cost = product["cost"] + ingredient["cost"]
            total_price = product["price"] + ingredient["price"]

            # Antwort zurücksenden
            await interaction.response.send_message(f"Gesamtberechnung:\nGesamtkosten: {total_cost}€\nGesamtpreis: {total_price}€", ephemeral=True)
        except Exception as e:
            print("Fehler bei der Berechnung:", e)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
