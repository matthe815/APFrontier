from typing import Dict, Any, Iterable, Optional, Union

from BaseClasses import Region, Entrance, Location, Item, Tutorial, CollectionState
from worlds.AutoWorld import World, WebWorld

client_version = 0

class BL2World(WebWorld):
    theme = "dirt"
    bug_report_page = "https://github.com/matthe815/Archipelago"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing BL2 with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Matthe815"]
    )]


class StardewValleyWorld(World):
    """
    BL2 is a game about picking up guns and shooting thing while picking up more guns and trying to save the vault from Handsome Jack.
    """
    game = "Stardew Valley"
    option_definitions = stardew_valley_options
    topology_present = False

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    data_version = 2
    required_client_version = (0, 4, 0)

    options: StardewOptions
    logic: StardewLogic

    web = StardewWebWorld()