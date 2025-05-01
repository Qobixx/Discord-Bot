import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from dotenv import load_dotenv
import os
import requests

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()



# Hole den Token aus der Umgebungsvariable
TOKEN = os.getenv("DISCORD_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# Intents (wichtig für Prefix-Commands & Modals)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Wetterdaten abrufen
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=de"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"🌤️ Wetter in {city.title()}: {weather}, {temp}°C"

# Modal zur Stadteingabe
class WeatherModal(Modal):
    def __init__(self):
        super().__init__(title="🌦️ Wetter abfragen")
        self.city = TextInput(label="Stadtname", placeholder="z. B. Berlin")
        self.add_item(self.city)

    async def on_submit(self, interaction: discord.Interaction):
        city_name = self.city.value.strip()
        result = get_weather(city_name)
        if result:
            await interaction.response.send_message(result, ephemeral=True)
        else:
            await interaction.response.send_message("❌ Stadt nicht gefunden oder API-Fehler.", ephemeral=True)

# Befehl zum Anzeigen des Buttons
@bot.command()
async def wetter(ctx):
    btn = Button(label="Wetter abfragen", style=discord.ButtonStyle.primary)
    view = View()
    view.add_item(btn)

    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(WeatherModal())

    btn.callback = button_callback
    await ctx.send("Klicke auf den Button, um das Wetter abzufragen:", view=view)

# Bot-Start
@bot.event
async def on_ready():
    print(f"✅ Bot gestartet als {bot.user}")

bot.run(TOKEN)
