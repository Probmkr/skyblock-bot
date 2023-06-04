import disnake
from disnake.ext import commands
from var import CmdBot
from lib import logger


class Other(commands.Cog):
    bot: CmdBot

    def __init__(self, bot: CmdBot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Bot started as {self.bot.user}")

    @commands.slash_command(name="help", description="show help")
    async def help(self, inter: disnake.AppCmdInter):
        await inter.response.send_message("there is nothing now")

    @commands.slash_command(name="ping", description="check ping")
    async def ping(self, inter: disnake.AppCmdInter):
        embed = disnake.Embed(
            title="Ping Result",
            color=disnake.Color.blue(),
            description=f"{int(self.bot.latency*1000)}ms",
        )
        await inter.response.send_message(embed=embed)


class Skyblock(commands.Cog):
    bot: CmdBot

    def __init__(self, bot: CmdBot) -> None:
        super().__init__()
        self.bot = bot


def setup(bot: CmdBot):
    bot.add_cog(Other(bot))
    bot.add_cog(Skyblock(bot))
