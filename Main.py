import discord
from discord.ext import commands
from discord.ui import Button, View, Select, SelectOption
from dotenv import load_dotenv
import os

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Hole den Token aus der Umgebungsvariable
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot initialisieren
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Beispiel für eine einfache Zutatenauswahl und Berechnung
produkte = {
    "OgKush": {"cost": 100, "price": 200},
    "Meht": {"cost": 150, "price": 300},
    "Cocain": {"cost": 500, "price": 1000},
}

zutaten = {
    "Gasolin": {"cost": 50, "price": 100},
    "Zucker": {"cost": 20, "price": 50},
    "Salz": {"cost": 10, "price": 20},
}

# Zutatenauswahl (jede Zutat einzeln)
class ZutatSelect(Select):
    def __init__(self):
        options = [SelectOption(label=zutat, value=zutat) for zutat in zutaten]
        super().__init__(placeholder="Wähle eine Zutat", options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_zutat = self.values[0]
        cost = zutaten[selected_zutat]["cost"]
        price = zutaten[selected_zutat]["price"]
        await interaction.response.send_message(
            f"Du hast die Zutat {selected_zutat} ausgewählt.\nKosten: {cost}€\nVerkaufspreis: {price}€",
            ephemeral=True,
        )

# Produkt auswählen
class ProduktSelect(Select):
    def __init__(self):
        options = [SelectOption(label=produkt, value=produkt) for produkt in produkte]
        super().__init__(placeholder="Wähle ein Produkt", options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_produkt = self.values[0]
        cost = produkte[selected_produkt]["cost"]
        price = produkte[selected_produkt]["price"]
        await interaction.response.send_message(
            f"Du hast das Produkt {selected_produkt} ausgewählt.\nKosten: {cost}€\nVerkaufspreis: {price}€",
            ephemeral=True,
        )


# !mix Befehl
@bot.command()
async def mix(ctx):
    # Button erstellen
    button = Button(label="Öffne Auswahlfenster!", style=discord.ButtonStyle.primary)

    # View erstellen und den Button hinzufügen
    view = View()
    view.add_item(button)

    async def button_callback(interaction: discord.Interaction):
        # Dropdown-Menüs für Produkt und Zutat erstellen
        produkt_select = ProduktSelect()
        zutat_select = ZutatSelect()

        # View für Produkt- und Zutatenauswahl
        view = View()
        view.add_item(produkt_select)
        view.add_item(zutat_select)

        await interaction.response.send_message("Wähle ein Produkt und eine Zutat:", view=view)

    button.callback = button_callback

    # Sende eine Nachricht mit dem Button
    await ctx.send("Klicke den Button, um das Auswahlfenster zu öffnen:", view=view)


# Bot bereit
@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")


bot.run(TOKEN)
