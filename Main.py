import discord
from discord.ext import commands
from discord.ui import Button, View, Select
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
zutaten = {
    "Gasolin": {"cost": 50, "price": 100},
    "Zucker": {"cost": 20, "price": 50},
    "Salz": {"cost": 10, "price": 20},
}

# Zutatenauswahl mit mehreren Optionen
class ZutatSelect(Select):
    def __init__(self):
        options = [discord.SelectOption(label=zutat, value=zutat) for zutat in zutaten]
        super().__init__(placeholder="Wähle eine oder mehrere Zutaten", options=options, min_values=1, max_values=len(zutaten))

    async def callback(self, interaction: discord.Interaction):
        selected_zutaten = self.values
        total_cost = 0
        total_price = 0
        for zutat in selected_zutaten:
            total_cost += zutaten[zutat]["cost"]
            total_price += zutaten[zutat]["price"]

        await interaction.response.send_message(
            f"Du hast die folgenden Zutaten ausgewählt: {', '.join(selected_zutaten)}.\nGesamtkosten: {total_cost}€\nGesamtverkaufspreis: {total_price}€",
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
        # Dropdown-Menü für Zutatenauswahl erstellen
        zutat_select = ZutatSelect()

        # View für Zutatenauswahl
        view = View()
        view.add_item(zutat_select)

        await interaction.response.send_message("Wähle eine oder mehrere Zutaten:", view=view)

    button.callback = button_callback

    # Sende eine Nachricht mit dem Button
    await ctx.send("Klicke den Button, um das Auswahlfenster zu öffnen:", view=view)


# Bot bereit
@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")


bot.run(TOKEN)
