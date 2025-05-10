import discord
from discord.ext import commands
from discord.ui import Button, View, Select  # Entferne SelectOption
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")  # Dein Bot-Token
FLASK_API_URL = "http://localhost:5000/calculate"  # Flask-API URL

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# Produkt- und Substanz-Optionen (direkt definieren, ohne SelectOption)
product_options = [
    discord.SelectOption(label="OG Kush", value="OgKush"),
    discord.SelectOption(label="Meth", value="Meth"),
    discord.SelectOption(label="Cocaine", value="Cocaine")
]

substance_options = [
    discord.SelectOption(label="Sugar", value="Sugar"),
    discord.SelectOption(label="Acetone", value="Acetone"),
    discord.SelectOption(label="Baking Soda", value="Baking Soda"),
    discord.SelectOption(label="Lemon", value="Lemon")
]

class ProductSelect(Select):
    def __init__(self):
        super().__init__(placeholder="Wähle ein Produkt", options=product_options)

    async def callback(self, interaction: discord.Interaction):
        interaction.user.selected_product = self.values[0]
        await interaction.response.send_message(f"Produkt {self.values[0]} ausgewählt!", ephemeral=True)

class SubstanceSelect(Select):
    def __init__(self):
        super().__init__(placeholder="Wähle Zutaten", options=substance_options, max_values=3)

    async def callback(self, interaction: discord.Interaction):
        interaction.user.selected_substances = self.values
        await interaction.response.send_message(f"Zutaten: {', '.join(self.values)} ausgewählt!", ephemeral=True)

class CalculateButton(Button):
    def __init__(self):
        super().__init__(label="Berechnen", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        product = interaction.user.selected_product
        substances = interaction.user.selected_substances

        # Anfrage an Flask-API senden
        response = requests.post(FLASK_API_URL, json={"product": product, "substances": substances})
        
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(title=f"Preisberechnung für {data['product']}", color=0x00ff00)
            embed.add_field(name="Kosten", value=f"{data['total_cost']} €", inline=True)
            embed.add_field(name="Verkaufspreis", value=f"{data['sell_price']} €", inline=True)
            embed.add_field(name="Gewinn", value=f"{data['profit']} €", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("Fehler bei der Berechnung. Bitte versuche es später erneut.", ephemeral=True)

@bot.command()
async def mix(ctx):
    # Hier fügst du jetzt die GUI für den Benutzer hinzu
    view = View()
    product_select = ProductSelect()
    substance_select = SubstanceSelect()
    calculate_button = CalculateButton()

    # Füge die GUI-Elemente zur Ansicht hinzu
    view.add_item(product_select)
    view.add_item(substance_select)
    view.add_item(calculate_button)

    # Sende die Nachricht im Discord-Chat mit der GUI
    await ctx.send("Wähle ein Produkt und die Zutaten aus, um den Preis zu berechnen:", view=view)

@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")

bot.run(TOKEN)
