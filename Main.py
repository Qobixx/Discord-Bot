import discord
from discord.ext import commands
from discord.ui import Modal, TextInput, View
from discord import app_commands
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

# Modal-Klasse
class MixModal(Modal):
    def __init__(self):
        super().__init__(title="Wähle ein Produkt und eine Zutat")
        
        # Produkt-Auswahl
        self.produkt_input = TextInput(
            label="Wähle ein Produkt", 
            placeholder="OgKush, Meht, Cocain",
            required=True
        )
        self.add_item(self.produkt_input)
        
        # Zutat-Auswahl
        self.zutat_input = TextInput(
            label="Wähle eine Zutat", 
            placeholder="Gasolin, Paper, Filter",
            required=True
        )
        self.add_item(self.zutat_input)
    
    async def callback(self, interaction: discord.Interaction):
        produkt = self.produkt_input.value
        zutat = self.zutat_input.value
        
        # Überprüfe, ob Produkt und Zutat existieren
        if produkt in produkte and zutat in zutaten:
            p = produkte[produkt]
            z = zutaten[zutat]

            ges_cost = p["cost"] + z["cost"]
            ges_price = p["price"] + z["price"]

            # Sende Ergebnis an den Benutzer
            await interaction.response.send_message(
                f"✅ **Auswahl abgeschlossen:**\n"
                f"🔹 Produkt: {produkt} (Kosten: {p['cost']}€, Preis: {p['price']}€)\n"
                f"🔹 Zutat: {zutat} (Kosten: {z['cost']}€, Preis: {z['price']}€)\n\n"
                f"💰 **Gesamtkosten:** {ges_cost}€\n"
                f"💵 **Gesamtpreis:** {ges_price}€",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Fehler: Ungültige Auswahl für Produkt oder Zutat.",
                ephemeral=True
            )

# !mix Befehl
@bot.command()
async def mix(ctx):
    # Erstelle Modal und sende es
    modal = MixModal()
    await ctx.send_modal(modal)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
