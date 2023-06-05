import json
import disnake
from disnake.ext import commands, tasks
from var import DATA_PREF, CmdBot
from lib import logger
from api import Bazaar, hpapi, mcapi
import re
import pprint
import lib


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


class Skyblock(commands.Cog):
    bot: CmdBot

    def __init__(self, bot: CmdBot) -> None:
        super().__init__()
        self.bot = bot
        self.fetch_bazaar.start()

    def cog_unload(self) -> None:
        self.fetch_bazaar.cancel()

    def search_for_list(self, search_string: str) -> list[str]:
        splited_search = search_string.split()
        data = lib.get_bazaar_data()

        def match(item: str):
            pat = f".*{'.*'.join(splited_search)}.*"
            match_obj = re.match(pat, item, re.IGNORECASE)
            return match_obj

        item_list = filter(match, data["products"].keys())
        return list(item_list)

    class BazaarDropdown(disnake.ui.StringSelect):
        sended: disnake.MessageInteraction

        def __init__(self, select_list: list[str]):
            options = [disnake.SelectOption(label=i) for i in select_list]
            super().__init__(
                placeholder="項目を選択してください...",
                min_values=1,
                max_values=len(options),
                options=options,
            )
            self.sended = None

        async def callback(self, inter: disnake.MessageInteraction):
            embeds: list[disnake.Embed] = []
            bazaar_data = lib.get_bazaar_data()["products"]
            for item in inter.values:
                item_data = bazaar_data[item]
                needed = [
                    "buyPrice",
                    "buyVolume",
                    "buyMovingWeek",
                    "sellPrice",
                    "sellVolume",
                    "sellMovingWeek",
                ]
                fields = [{"name": i, "value": f'`{int(item_data["quick_status"][i]):,}`'} for i in needed]
                embeds.append(
                    lib.get_embed(
                        embed_type="info",
                        title=item,
                        description=f"`{item}` の詳細",
                        inline=True,
                        fields=fields,
                        url=f"https://skyblock.finance/items/{item}"
                    )
                )
            logger.debug(self.sended, "sended")
            if self.sended:
                await self.sended.edit_original_message(embeds=embeds)
                await inter.response.send_message()
                await inter.delete_original_message()
            else:
                await inter.response.send_message(embeds=embeds)
                self.sended = inter

    @tasks.loop(minutes=5)
    async def fetch_bazaar(self):
        data = await hpapi.fetch_bazaar()
        lib.set_bazaar_data(data)
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
        item_list = self.search_for_list(search_string)
        try:
            await inter.response.send_message(f"`{item_list}`")
        except disnake.errors.HTTPException:
            await inter.response.send_message(
                embed=lib.get_embed(embed_type="error", description="結果が多すぎます")
            )

    @bazaar.sub_command(
        name="detail",
        description="get detail of items",
        options=[
            disnake.Option(
                name="search_string",
                description="separated by space",
                type=disnake.OptionType.string,
                required=True,
            )
        ],
    )
    async def detail(self, inter: disnake.AppCmdInter, search_string: str):
        item_list = self.search_for_list(search_string)
        if 20 < len(item_list):
            await inter.response.send_message(
                embed=lib.get_embed(
                    embed_type="error", description="結果が多すぎます\n20個以内に絞り込んでください"
                )
            )
            return
        elif len(item_list) < 1:
            await inter.response.send_message(
                embed=lib.get_embed(embed_type="error", description="見つかりませんでした")
            )
            return
        view = disnake.ui.View()
        select = self.BazaarDropdown(item_list)
        view.add_item(select)
        view.on_error = None
        await inter.response.send_message(view=view)


def setup(bot: CmdBot):
    bot.add_cog(Other(bot))
    bot.add_cog(Skyblock(bot))
