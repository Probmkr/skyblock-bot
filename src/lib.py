import json
from typing import Any, Literal
from api import Bazaar, Items
from logger import Logger
import disnake

from var import DATA_PREF


logger = Logger()

bazaar_data_path = f"{DATA_PREF}/bazaar.json"
item_data_path = f"{DATA_PREF}/items.json"


def get_bazaar_data():
    data: Bazaar = json.load(open(bazaar_data_path))
    return data

def set_bazaar_data(data: Bazaar):
    json.dump(data, open(bazaar_data_path, "w"))

def get_items_data():
    data: Items = json.load(open(item_data_path))
    return data

def set_items_data(data: Items):
    json.dump(data, open(item_data_path, "w"))

ITEMS_DATA = get_items_data()

embed_types = {
    "error": {"title": "Error", "color": disnake.Color.red()},
    "warning": {"title": "Warning", "color": disnake.Color.orange()},
    "info": {"title": "Info", "color": 0x00FFFF},
    "success": {"title": "Success", "color": disnake.Color.green()},
}


def get_embed(
    *,
    embed_type: Literal["error", "warning", "info", "success"] | None,
    title: str | None = None,
    description: str | None = None,
    color: int | disnake.Color = None,
    fields: dict[str, Any] = [],
    inline: bool = False,
    **other
) -> disnake.Embed:
    embed = disnake.Embed(
        title=title or embed_types[embed_type]["title"],
        description=description,
        color=color or embed_types[embed_type]["color"],
        **other
    )
    for field in fields:
        embed.add_field(**field, inline=inline)
    return embed
