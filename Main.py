import discord
from discord.ext import commands
from discord.ui import Select, View
from dotenv import load_dotenv
import os

# .env laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Produkt- und Zutatendaten
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

# Speichert Auswahl pro User
user_auswahl = {}

# Produkt-Dropdown
class ProduktDropdown(Select):
    def __init__(self):
        options = [discord.SelectOption(label=name, value=name) for name in produkte]
        super().__init__(placeholder="Wähle ein Produkt", options=options)

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_auswahl.setdefault(user_id, {})
        user_auswahl[user_id]["produkt"] = self.values[0]
        await sende_auswertung(interaction, user_id)

# Zutaten-Dropdown
class ZutatDropdown(Select):
    def __init__(self):
        options = [discord.SelectOption(label=name, value=name) for name in zutaten]
        super().__init__(placeholder="Wähle eine Zutat", options=options)

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_auswahl.setdefault(user_id, {})
        user_auswahl[user_id]["zutat"] = self.values[0]
        await sende_auswertung(interaction, user_id)

# Funktion zur Ergebnisanzeige
async def sende_auswertung(interaction, user_id):
    auswahl = user_auswahl[user_id]
    if "produkt" in auswahl and "zutat" in auswahl:
        produkt = auswahl["produkt"]
        zutat = auswahl["zutat"]
        p = produkte[produkt]
        z = zutaten[zutat]

        ges_cost = p["cost"] + z["cost"]
        ges_price = p["price"] + z["price"]

        await interaction.response.send_message(
            f"🔹 **Produkt**: {produkt} (Kosten: {p['cost']}€, Preis: {p['price']}€)\n"
            f"🔹 **Zutat**: {zutat} (Kosten: {z['cost']}€, Preis: {z['price']}€)\n\n"
            f"💰 **Gesamtkosten:** {ges_cost}€\n"
            f"💵 **Gesamtpreis:** {ges_price}€",
            ephemeral=True
        )

# !mix Befehl
@bot.command()
async def mix(ctx):
    view = View()
    view.add_item(ProduktDropdown())
    view.add_item(ZutatDropdown())
    await ctx.send("🔧 Wähle ein Produkt und eine Zutat aus:", view=view)

# Bot ready
@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
