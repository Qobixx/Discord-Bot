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

# Beispiel für Produkte und Zutaten
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

# Produkt-Auswahl
class ProduktSelect(Select):
    def __init__(self):
        options = [discord.SelectOption(label=produkt, value=produkt) for produkt in produkte]
        super().__init__(placeholder="Wähle ein Produkt", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Speichern der Auswahl des Produkts in der Interaktionsantwort
        self.product = self.values[0]
        await interaction.response.send_message(f"Du hast das Produkt '{self.product}' ausgewählt.", ephemeral=True)


# Zutatenauswahl mit mehreren Auswahlmöglichkeiten
class ZutatSelect(Select):
    def __init__(self):
        options = [discord.SelectOption(label=zutat, value=zutat) for zutat in zutaten]
        super().__init__(placeholder="Wähle eine oder mehrere Zutaten", options=options, min_values=1, max_values=len(zutaten))

    async def callback(self, interaction: discord.Interaction):
        # Speichern der Auswahl der Zutaten in der Interaktionsantwort
        self.zutaten = self.values
        await interaction.response.send_message(f"Du hast die Zutaten {', '.join(self.zutaten)} ausgewählt.", ephemeral=True)


# Berechnung und Ausgabe des Gesamtpreises
class CalculateButton(Button):
    def __init__(self):
        super().__init__(label="Berechnen", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        # Berechnung des Gesamtpreises
        if not hasattr(self, 'product') or not hasattr(self, 'zutaten'):
            await interaction.response.send_message("Bitte wähle sowohl ein Produkt als auch eine Zutat aus, bevor du auf 'Berechnen' klickst.", ephemeral=True)
            return
        
        # Berechne die Gesamtkosten
        product_cost = produkte[self.product]["cost"]
        total_cost = product_cost
        
        # Kosten für jede ausgewählte Zutat
        for zutat in self.zutaten:
            total_cost += zutaten[zutat]["cost"]

        # Zeige die Gesamtkosten an
        await interaction.response.send_message(f"Die Gesamtkosten betragen {total_cost}€.", ephemeral=True)


# !mix Befehl
@bot.command()
async def mix(ctx):
    # Button erstellen
    button = Button(label="Öffne Auswahlfenster!", style=discord.ButtonStyle.primary)

    # View erstellen und den Button hinzufügen
    view = View()
    view.add_item(button)

    async def button_callback(interaction: discord.Interaction):
        # Dropdown-Menü für Produkt und Zutaten
        produkt_select = ProduktSelect()
        zutat_select = ZutatSelect()
        calculate_button = CalculateButton()

        # View für Produkt- und Zutatenauswahl
        selection_view = View()
        selection_view.add_item(produkt_select)
        selection_view.add_item(zutat_select)
        selection_view.add_item(calculate_button)

        # Berechnung durchführen, wenn der "Berechnen"-Button gedrückt wird
        async def calculate_callback(interaction: discord.Interaction):
            # Überprüfen, ob sowohl Produkt als auch Zutaten ausgewählt wurden
            if not hasattr(produkt_select, 'values') or not hasattr(zutat_select, 'values'):
                await interaction.response.send_message("Bitte wähle sowohl ein Produkt als auch eine Zutat aus, bevor du auf 'Berechnen' klickst.", ephemeral=True)
                return

            # Die Produkt- und Zutatenauswahl wird in der Berechnung berücksichtigt
            product = produkt_select.values[0]
            zutaten = zutat_select.values

            # Berechnung des Gesamtpreises
            product_cost = produkte[product]["cost"]
            total_cost = product_cost

            # Addiere die Kosten für die Zutaten
            for zutat in zutaten:
                total_cost += zutaten[zutat]["cost"]

            # Gesamtkosten anzeigen
            await interaction.response.send_message(f"Die Gesamtkosten betragen {total_cost}€.", ephemeral=True)

        # Setzen des calculate_callback für den Button
        calculate_button.callback = calculate_callback
        
        await interaction.response.send_message("Wähle ein Produkt und eine oder mehrere Zutaten, dann klicke auf 'Berechnen':", view=selection_view)

    # Setzen des button_callback für den Button
    button.callback = button_callback

    # Sende eine Nachricht mit dem Button
    await ctx.send("Klicke den Button, um das Auswahlfenster zu öffnen:", view=view)


# Bot bereit
@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")


bot.run(TOKEN)
