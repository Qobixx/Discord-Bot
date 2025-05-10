import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from dotenv import load_dotenv
import os

# .env laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Produkte und Zutaten (jeweils mit cost und price)
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

# Auswahl-Menü für beides
class AuswahlSelect(Select):
    def __init__(self):
        options = []
        for name, data in produkte.items():
            options.append(discord.SelectOption(label=f"Produkt: {name}", value=f"produkt:{name}"))
        for name, data in zutaten.items():
            options.append(discord.SelectOption(label=f"Zutat: {name}", value=f"zutat:{name}"))

        super().__init__(placeholder="Wähle ein Produkt oder eine Zutat", options=options)

    async def callback(self, interaction: discord.Interaction):
        typ, name = self.values[0].split(":")
        data = produkte[name] if typ == "produkt" else zutaten[name]

        await interaction.response.send_message(
            f"**{typ.capitalize()}**: {name}\n"
            f"- Kosten: {data['cost']}€\n"
            f"- Preis: {data['price']}€",
            ephemeral=True
        )

# !auswahl Befehl
@bot.command()
async def auswahl(ctx):
    button = Button(label="Auswahl öffnen", style=discord.ButtonStyle.primary)
    view = View()
    view.add_item(button)

    async def button_callback(interaction: discord.Interaction):
        select = AuswahlSelect()
        select_view = View()
        select_view.add_item(select)
        await interaction.response.send_message("Wähle aus:", view=select_view)

    button.callback = button_callback
    await ctx.send("Klicke auf den Button, um ein Produkt oder eine Zutat auszuwählen:", view=view)

# Start
@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
