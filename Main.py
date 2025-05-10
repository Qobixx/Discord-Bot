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
    "Water": {"cost": 5, "price": 10}
}

# Funktionsweise der Auswahl für Produkte
class ProduktSelect(Select):
    def __init__(self):
        options = [discord.SelectOption(label=produkt, value=produkt) for produkt in produkte]
        super().__init__(placeholder="Wähle ein Produkt", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Produktwert speichern, wenn es ausgewählt wird
        self.view.selected_product = self.values[0]  # Speichern der Auswahl
        # Nachricht senden, welche Auswahl getroffen wurde
        await interaction.response.send_message(f"Du hast das Produkt **{self.view.selected_product}** ausgewählt.", ephemeral=True)


# Funktionsweise der Auswahl für Zutaten (mit Mehrfachauswahl)
class ZutatSelect(Select):
    def __init__(self):
        options = [discord.SelectOption(label=zutat, value=zutat) for zutat in zutaten]
        super().__init__(placeholder="Wähle eine oder mehrere Zutaten", options=options, min_values=1, max_values=len(zutaten), row=1, multiple=True)

    async def callback(self, interaction: discord.Interaction):
        # Zutatwert speichern, wenn es ausgewählt wird
        self.view.selected_ingredients = self.values  # Speichern der Auswahl
        # Nachricht senden, welche Auswahl getroffen wurde
        await interaction.response.send_message(f"Du hast die Zutaten {', '.join(self.view.selected_ingredients)} ausgewählt.", ephemeral=True)


# Berechnen-Button
class CalculateButton(Button):
    def __init__(self):
        super().__init__(label="Berechnen", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        # Überprüfen, ob sowohl Produkt als auch Zutat(en) ausgewählt wurden
        if not hasattr(self.view, "selected_product") or not hasattr(self.view, "selected_ingredients"):
            await interaction.response.send_message(
                "Bitte wähle sowohl ein Produkt als auch eine Zutat(en) aus, bevor du auf 'Berechnen' klickst.",
                ephemeral=True
            )
            return

        product = self.view.selected_product
        ingredients = self.view.selected_ingredients

        # Berechnung der Gesamtkosten und Gesamtpreis
        product_cost = produkte[product]["cost"]
        product_price = produkte[product]["price"]
        total_cost = product_cost
        total_price = product_price

        # Kosten und Preise für alle Zutaten addieren
        for ingredient in ingredients:
            ingredient_cost = zutaten[ingredient]["cost"]
            ingredient_price = zutaten[ingredient]["price"]
            total_cost += ingredient_cost
            total_price += ingredient_price

        # Berechnete Werte zurückgeben
        await interaction.response.send_message(
            f"Du hast das Produkt **{product}** und die Zutaten {', '.join(ingredients)} ausgewählt.\n"
            f"Gesamtkosten: {total_cost}€\nGesamtpreis: {total_price}€"
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
        # Neue Ansicht mit Produkt- und Zutatenauswahl + Berechnen-Button erstellen
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
            "Wähle ein Produkt und eine oder mehrere Zutaten aus, und klicke dann auf 'Berechnen', um die Preise zu sehen.",
            view=new_view
        )

    button.callback = button_callback

    # Sende eine Nachricht mit dem Button
    await ctx.send("Klicke auf den Button, um ein Produkt und eine oder mehrere Zutaten auszuwählen:", view=view)


@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
