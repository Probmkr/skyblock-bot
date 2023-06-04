import disnake
from disnake.ext import commands
from env import *

bot = commands.Bot(command_prefix="sky!", intents=disnake.Intents.all())
bot.load_extension("cogs")
