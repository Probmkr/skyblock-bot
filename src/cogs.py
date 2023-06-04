import json
import disnake
from disnake.ext import commands, tasks
from var import DATA_PREF, CmdBot
from lib import logger
from api import Bazaar, hpapi, mcapi
import re


class Other(commands.Cog):
    bot: CmdBot

    def __init__(self, bot: CmdBot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Bot started as {self.bot.user}", "startbot")

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


bazaar_data_path = f"{DATA_PREF}/bazaar.json"


class Skyblock(commands.Cog):
    bot: CmdBot

    def __init__(self, bot: CmdBot) -> None:
        super().__init__()
        self.bot = bot
        self.fetch_bazaar.start()

    def cog_unload(self) -> None:
        self.fetch_bazaar.cancel()

    @tasks.loop(minutes=5)
    async def fetch_bazaar(self):
        data = await hpapi.fetch_bazaar()
        json.dump(data, open(bazaar_data_path, "w"))
        logger.debug("updated bazaar data", "bazaar_cog")

    @commands.slash_command(name="bazaar", description="commands about bazaar")
    async def bazaar(self, inter):
        pass

    @bazaar.sub_command(
        name="search",
        description="search item id",
        options=[
            disnake.Option(
                name="search_string",
                description="separated by space",
                type=disnake.OptionType.string,
                required=True,
            )
        ],
    )
    async def search(self, inter: disnake.AppCmdInter, search_string: str):
        splited_search = search_string.split()
        logger.debug(splited_search, "baz_sear")
        data: Bazaar = json.load(open(bazaar_data_path))
        def match(item: str):
            pat = f".*{'.*'.join(splited_search)}.*"
            match_obj = re.match(pat, item, re.IGNORECASE)
            return match_obj
        item_list = filter(match, data["products"].keys())
        try:
            await inter.response.send_message(f"`{list(item_list)}`")
        except disnake.errors.HTTPException:
            await inter.response.send_message("結果が多すぎます")


def setup(bot: CmdBot):
    bot.add_cog(Other(bot))
    bot.add_cog(Skyblock(bot))
