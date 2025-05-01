import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from dotenv import load_dotenv
import os
import requests
from datetime import datetime

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()



# Hole den Token aus der Umgebungsvariable
TOKEN = os.getenv("DISCORD_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
bot = commands.Bot(command_prefix="!", intents=intents)


# Wetterdaten für 4 Tage abrufen
def get_4_day_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=de"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()
    forecast = []

    for entry in data["list"]:
        dt_txt = entry["dt_txt"]
        if "12:00:00" in dt_txt:  # nur die Mittagsdaten (1x pro Tag)
            day = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S").strftime("%A, %d.%m.")
            temp = entry["main"]["temp"]
            desc = entry["weather"][0]["description"].capitalize()
            icon = entry["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            forecast.append((day, temp, desc, icon_url))
            if len(forecast) == 4:
                break
    return forecast

# Modal für Stadteingabe
class WeatherModal(Modal):
    def __init__(self):
        super().__init__(title="🌦️ Wettervorhersage")
        self.city = TextInput(label="Stadtname", placeholder="z. B. Berlin")
        self.add_item(self.city)

    async def on_submit(self, interaction: discord.Interaction):
        city_name = self.city.value.strip()
        forecast = get_4_day_forecast(city_name)
        if not forecast:
            await interaction.response.send_message("❌ Stadt nicht gefunden oder API-Fehler.", ephemeral=True)
            return

        embed = discord.Embed(title=f"📅 Wetter für {city_name.title()} – 4 Tage Vorschau", color=0x1abc9c)
        for day, temp, desc, icon_url in forecast:
            embed.add_field(name=day, value=f"{desc}, **{temp:.1f}°C**", inline=False)
            embed.set_thumbnail(url=forecast[0][3])  # Icon vom ersten Tag

        await interaction.response.send_message(embed=embed, ephemeral=True)

# Button anzeigen
@bot.command()
async def wetter(ctx):
    btn = Button(label="Wetter abfragen", style=discord.ButtonStyle.primary)
    view = View()
    view.add_item(btn)

    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(WeatherModal())

    btn.callback = button_callback
    await ctx.send("🌤️ Klicke auf den Button, um eine Wettervorhersage zu bekommen:", view=view)

# Bot gestartet
@bot.event
async def on_ready():
    print(f"✅ Bot online als {bot.user}")

bot.run(TOKEN)
