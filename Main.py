import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from dotenv import load_dotenv
import os
import asyncio

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
        # Produktwert speichern, wenn es ausgewählt wird
        self.view.selected_product = self.values[0]  # Speichern der Auswahl
        # Keine Nachricht senden


# Funktionsweise der Auswahl für Zutaten
class ZutatSelect(Select):
    def __init__(self):
        options = [discord.SelectOption(label=zutat, value=zutat) for zutat in zutaten]
        super().__init__(placeholder="Wähle eine Zutat", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Zutatwert speichern, wenn es ausgewählt wird
        self.view.selected_ingredient = self.values[0]  # Speichern der Auswahl
        # Keine Nachricht senden


# Berechnen-Button
class CalculateButton(Button):
    def __init__(self):
        super().__init__(label="Berechnen", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        # Überprüfen, ob sowohl Produkt als auch Zutat ausgewählt wurden
        if not hasattr(self.view, "selected_product") or not hasattr(self.view, "selected_ingredient"):
            # Wenn nicht beide ausgewählt sind, eine Nachricht senden und diese löschen
            no_selection_msg = await interaction.response.send_message(
                "Bitte wähle sowohl ein Produkt als auch eine Zutat aus, bevor du auf 'Berechnen' klickst.",
                ephemeral=True
            )
            await asyncio.sleep(3)
            await no_selection_msg.delete()
            return

        product = self.view.selected_product
        ingredient = self.view.selected_ingredient

        # Berechnung der Gesamtkosten und Gesamtpreis
        product_cost = produkte[product]["cost"]
        product_price = produkte[product]["price"]
        ingredient_cost = zutaten[ingredient]["cost"]
        ingredient_price = zutaten[ingredient]["price"]

        # Gesamtkosten und Gesamtpreis
        total_cost = product_cost + ingredient_cost
        total_price = product_price + ingredient_price

        # Berechnete Werte zurückgeben und alle anderen Nachrichten löschen
        result_msg = await interaction.response.send_message(
            f"Du hast das Produkt **{product}** und die Zutat **{ingredient}** ausgewählt.\n"
            f"Gesamtkosten: {total_cost}€\nGesamtpreis: {total_price}€"
        )

        # Alle Nachrichten, die vor der Berechnung gesendet wurden, löschen
        for message in interaction.message.channel.history(limit=2):
            if message != result_msg:
                await message.delete()


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
        # Neue Ansicht mit Produkt- und Zutatenauswahl erstellen
        produkt_select = ProduktSelect()
        zutat_select = ZutatSelect()
        calculate_button = CalculateButton()

        # Neue View für Produkt- und Zutatenauswahl + Berechnen-Button erstellen
        new_view = View()
        new_view.add_item(produkt_select)
        new_view.add_item(zutat_select)
        new_view.add_item(calculate_button)  # Berechnen Button

        # Nachricht senden, dass der Benutzer ein Produkt und eine Zutat wählen soll
        await interaction.response.send_message(
            "Wähle ein Produkt und eine Zutat aus, und klicke dann auf 'Berechnen', um die Preise zu sehen.",
            view=new_view
        )

    button.callback = button_callback

    # Sende eine Nachricht mit dem Button
    await ctx.send("Klicke auf den Button, um ein Produkt und eine Zutat auszuwählen:", view=view)


@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
