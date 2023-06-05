import disnake
from disnake.ext import commands
from cogs import Other, Skyblock
from env import *
from lib import logger

bot = commands.Bot(command_prefix="sky!", intents=disnake.Intents.all(), reload=True)
## use extension
# bot.load_extension("cogs")
## not use extension
bot.add_cog(Skyblock(bot))
bot.add_cog(Other(bot))

@bot.event
async def on_interaction(inter: disnake.AppCmdInter):
    if isinstance(inter, disnake.AppCmdInter):
        logger.trace(f"user `{inter.author}` triggered command `/{inter.application_command.qualified_name}`")
