import disnake
from disnake.ext import commands
from env import *
from lib import logger

bot = commands.Bot(command_prefix="sky!", intents=disnake.Intents.all(), reload=True)
bot.load_extension("cogs")

@bot.event
async def on_interaction(inter: disnake.AppCmdInter):
    if isinstance(inter, disnake.AppCmdInter):
        logger.debug(f"user `{inter.author}` triggered command `/{inter.application_command}`")
