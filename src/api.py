from typing import Literal, TypedDict
import aiohttp
from env import API_KEY
from logger import Logger

logger = Logger()


class MCAPI:
    api_pref: str

    def __init__(self) -> None:
        self.api_pref = "https://api.mojang.com"

    async def fetchUUID(self, player_name: str) -> str | bool:
        endpoint = f"/users/profiles/minecraft/{player_name}"
        async with aiohttp.ClientSession(self.api_pref) as session:
            res = await session.get(endpoint)
            if res.status == 204:
                return False
            json = await res.json()
            return json["id"]


class Stats(TypedDict):
    pass


class Item(TypedDict):
    material: str
    durability: int
    skin: str
    name: str
    glowing: bool
    category: str
    tier: Literal["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC", "DIVINE", "VERY SPECIAL"]
    npc_cell_price: int
    id: str


class Items(TypedDict):
    success: bool
    lastUpdated: int
    items: dict[str, Item]


class BazaarSummary(TypedDict):
    amount: int
    pricePerUnit: float
    orders: int


class BazaarQuickStatus(TypedDict):
    productId: str
    sellPrice: float
    sellVolume: int
    sellMovingWeek: int
    sellOrders: int
    buyPrice: float
    buyVolume: int
    buyMovingWeek: int
    buyOrders: int


class BazaarProducts(TypedDict):
    product_id: str
    sell_summary: list[BazaarSummary]
    buy_summary: list[BazaarSummary]
    quick_status: BazaarQuickStatus


class Bazaar(TypedDict):
    success: bool
    lastUpdated: int
    products: dict[str, BazaarProducts]


class HypixelAPI:
    key: str
    api_pref: str

    def __init__(self, key: str = API_KEY) -> None:
        self.key = key
        self.api_pref = "https://api.hypixel.net"

    def get_session(self):
        return aiohttp.ClientSession(self.api_pref)

    async def fetch_items(self) -> Items | bool:
        async with self.get_session() as session:
            endpoint = "/resources/skyblock/items"
            res = await session.get(endpoint)
            if res.status == 200:
                json = await res.json()
                items = json["items"]
                json["items"] = {i["id"]: i for i in items}
                return json
            else:
                return False

    async def fetch_bazaar(self) -> Bazaar | bool:
        async with self.get_session() as session:
            endpoint = "/skyblock/bazaar"
            res = await session.get(endpoint)
            if res.status == 200:
                json = await res.json()
                return json
            else:
                return False


mcapi = MCAPI()
hpapi = HypixelAPI(API_KEY)
