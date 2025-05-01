import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from dotenv import load_dotenv
import os
import yt_dlp as youtube_dl
import asyncio

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()



# Hole den Token aus der Umgebungsvariable
TOKEN = os.getenv("DISCORD_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Audio-Setup für yt-dlp und Voice-Channel
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioquality': 1,
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'quiet': True,
        }
        loop = loop or asyncio.get_event_loop()

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            title = info.get('title')
            source = await discord.FFmpegOpusAudio.from_probe(url2)
            return cls(source, data=info)

# Bot-Befehl für YouTube-Audio
@bot.command()
async def play(ctx, url: str):
    """Spielt ein YouTube-Video im Voice Channel."""
    if not ctx.message.author.voice:
        await ctx.send("Du musst in einem Voice Channel sein, um Musik zu hören.")
        return

    channel = ctx.message.author.voice.channel
    voice_client = await channel.connect()

    # Lade die Audioquelle von YouTube
    player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
    
    # Spiele die Audioquelle
    voice_client.play(player, after=lambda e: print('done', e))

    await ctx.send(f"Spiele jetzt: {player.title}")

    # Wenn das Audio zu Ende ist, trenne die Verbindung nach 5 Sekunden
    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()

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

# Modal für Stadteingabe (Wetter)
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

# Button anzeigen für Wetter
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
