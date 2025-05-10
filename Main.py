import discord
from discord.ext import commands
from discord.ui import View, Select
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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

class MixView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.produkt = None
        self.zutat = None

        self.produkt_select = Select(
            placeholder="🧪 Produkt wählen",
            options=[discord.SelectOption(label=p) for p in produkte],
            min_values=1, max_values=1
        )
        self.produkt_select.callback = self.produkt_chosen

        self.zutat_select = Select(
            placeholder="🧂 Zutat wählen",
            options=[discord.SelectOption(label=z) for z in zutaten],
            min_values=1, max_values=1
        )
        self.zutat_select.callback = self.zutat_chosen

        self.add_item(self.produkt_select)
        self.add_item(self.zutat_select)

    async def produkt_chosen(self, interaction: discord.Interaction):
        self.produkt = self.produkt_select.values[0]
        await self.try_send_result(interaction)

    async def zutat_chosen(self, interaction: discord.Interaction):
        self.zutat = self.zutat_select.values[0]
        await self.try_send_result(interaction)

    async def try_send_result(self, interaction: discord.Interaction):
        if self.produkt and self.zutat:
            p = produkte[self.produkt]
            z = zutaten[self.zutat]

            total_cost = p["cost"] + z["cost"]
            total_price = p["price"] + z["price"]

            await interaction.response.send_message(
                f"✅ **Auswahl abgeschlossen:**\n"
                f"🔹 Produkt: {self.produkt} (Kosten: {p['cost']}€, Preis: {p['price']}€)\n"
                f"🔹 Zutat: {self.zutat} (Kosten: {z['cost']}€, Preis: {z['price']}€)\n\n"
                f"💰 **Gesamtkosten:** {total_cost}€\n"
                f"💵 **Gesamtpreis:** {total_price}€",
                ephemeral=True
            )

@bot.command()
async def mix(ctx):
    view = MixView()
    await ctx.send("🔧 Bitte wähle Produkt und Zutat aus:", view=view)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(TOKEN)
