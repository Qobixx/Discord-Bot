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

# Daten
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

# Globale Auswahl speichern
user_auswahl = {}

# Produkt-Dropdown
class ProduktDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=name, value=name) for name in produkte
        ]
        super().__init__(placeholder="Wähle ein Produkt", options=options)

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_auswahl.setdefault(user_id, {})
        user_auswahl[user_id]['produkt'] = self.values[0]
        await sende_auswertung(interaction, user_id)

# Zutaten-Dropdown
class ZutatDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=name, value=name) for name in zutaten
        ]
        super().__init__(placeholder="Wähle eine Zutat", options=options)

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_auswahl.setdefault(user_id, {})
        user_auswahl[user_id]['zutat'] = self.values[0]
        await sende_auswertung(interaction, user_id)

# Auswertung senden wenn beides gewählt
async def sende_auswertung(interaction, user_id):
    auswahl = user_auswahl[user_id]
    if 'produkt' in auswahl and 'zutat' in auswahl:
        produkt = auswahl['produkt']
        zutat = auswahl['zutat']

        p_data = produkte[produkt]
        z_data = zutaten[zutat]

        ges_cost = p_data['cost'] + z_data['cost']
        ges_price = p_data['price'] + z_data['price']

        await interaction.response.send_message(
            f"**Produkt**: {produkt} (Kosten: {p_data['cost']}€, Preis: {p_data['price']}€)\n"
            f"**Zutat**: {zutat} (Kosten: {z_data['cost']}€, Preis: {z_data['price']}€)\n\n"
            f"📦 **Gesamtkosten:** {ges_cost}€\n💰 **Gesamtpreis:** {ges_price}€",
            ephemeral=True
        )

# Befehl starten
@bot.command()
async def kombi(ctx):
    view = View()
    view.add_item(ProduktDropdown())
    view.add_item(ZutatDropdown())
    await ctx.send("Wähle ein Produkt und eine Zutat aus:", view=view)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
