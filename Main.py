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

# Produkt- und Zutaten-Daten
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
        options = [discord.SelectOption(label=produkt, value=produkt) for produkt in produkte]
        super().__init__(placeholder="Wähle ein Produkt", options=options)

    async def callback(self, interaction: discord.Interaction):
        self.product = self.values[0]  # Das ausgewählte Produkt speichern
        await interaction.response.send_message(f"Du hast das Produkt **{self.product}** ausgewählt! Bitte wähle nun eine Zutat.", ephemeral=True)

# Funktionsweise der Auswahl für Zutaten
class ZutatSelect(Select):
    def __init__(self):
        options = [discord.SelectOption(label=zutat, value=zutat) for zutat in zutaten]
        super().__init__(placeholder="Wähle eine Zutat", options=options)

    async def callback(self, interaction: discord.Interaction):
        self.ingredient = self.values[0]  # Die ausgewählte Zutat speichern
        await interaction.response.send_message(f"Du hast die Zutat **{self.ingredient}** ausgewählt! Klicke nun auf 'Berechnen', um die Kosten zu sehen.", ephemeral=True)

# Berechnen-Button
class CalculateButton(Button):
    def __init__(self):
        super().__init__(label="Berechnen", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        # Berechnung der Gesamtkosten und Gesamtpreis
        product_cost = produkte[self.product]["cost"]
        product_price = produkte[self.product]["price"]
        ingredient_cost = zutaten[self.ingredient]["cost"]
        ingredient_price = zutaten[self.ingredient]["price"]

        # Gesamtkosten und Gesamtpreis
        total_cost = product_cost + ingredient_cost
        total_price = product_price + ingredient_price

        # Berechnete Werte zurückgeben
        await interaction.response.send_message(
            f"Du hast das Produkt **{self.product}** und die Zutat **{self.ingredient}** ausgewählt.\n"
            f"Gesamtkosten: {total_cost}€\nGesamtpreis: {total_price}€",
            ephemeral=True
        )

# !mix Befehl
@bot.command()
async def mix(ctx):
    # Button erstellen, um Auswahlfenster zu öffnen
    button = Button(label="Öffne Auswahlfenster!", style=discord.ButtonStyle.primary)

    # View erstellen und den Button hinzufügen
    view = View()
    view.add_item(button)

    # Wenn der Button geklickt wird, zeige Produkt- und Zutatenauswahl an
    async def button_callback(interaction: discord.Interaction):
        produkt_select = ProduktSelect()
        zutat_select = ZutatSelect()
        
        # Berechnen-Button erst nach Auswahl anzeigen
        calculate_button = CalculateButton()  # Berechnen-Button
        
        # Eine neue View mit Auswahl und Berechnen-Button erstellen
        view = View()
        view.add_item(produkt_select)
        view.add_item(zutat_select)
        view.add_item(calculate_button)  # Berechnen Button

        # Nachricht senden, dass der Benutzer ein Produkt und eine Zutat wählen soll
        await interaction.response.send_message(
            "Wähle ein Produkt und eine Zutat aus, und klicke dann auf 'Berechnen', um die Preise zu sehen.",
            view=view
        )

    button.callback = button_callback

    # Sende eine Nachricht mit dem Button
    await ctx.send("Klicke auf den Button, um ein Produkt und eine Zutat auszuwählen:", view=view)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
