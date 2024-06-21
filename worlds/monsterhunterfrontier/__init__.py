import os
import json
import settings
import typing
from base64 import b64encode, b64decode
from typing import Dict, Any

from BaseClasses import Region, MultiWorld, Entrance, Item, Tutorial, ItemClassification, Location
from worlds.AutoWorld import World, WebWorld

from . import Constants
from .Options import minecraft_options
from .ItemPool import build_item_pool, get_junk_item_names
from .Rules import set_rules

client_version = 9


class MHFSettings(settings.Group):
    class ReleaseChannel(str):
        """
        release channel, currently "release", or "beta"
        any games played on the "beta" channel have a high likelihood of no longer working on the "release" channel.
        """
    release_channel: ReleaseChannel = ReleaseChannel("release")


class MinecraftWebWorld(WebWorld):
    theme = "jungle"
    bug_report_page = "https://github.com/KonoTyran/Minecraft_AP_Randomizer/issues/new?assignees=&labels=bug&template=bug_report.yaml&title=%5BBug%5D%3A+Brief+Description+of+bug+here"

    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Minecraft software on your computer. This guide covers"
        "single-player, multiworld, and related software.",
        "English",
        "minecraft_en.md",
        "minecraft/en",
        ["Kono Tyran"]
    )

    setup_es = Tutorial(
        setup.tutorial_name,
        setup.description,
        "Español",
        "minecraft_es.md",
        "minecraft/es",
        ["Edos"]
    )

    setup_sv = Tutorial(
        setup.tutorial_name,
        setup.description,
        "Swedish",
        "minecraft_sv.md",
        "minecraft/sv",
        ["Albinum"]
    )

    setup_fr = Tutorial(
        setup.tutorial_name,
        setup.description,
        "Français",
        "minecraft_fr.md",
        "minecraft/fr",
        ["TheLynk"]
    )

    tutorials = [setup, setup_es, setup_sv, setup_fr]


class MHFWorld(World):
    """
    Minecraft is a game about creativity. In a world made entirely of cubes, you explore, discover, mine,
    craft, and try not to explode. Delve deep into the earth and discover abandoned mines, ancient
    structures, and materials to create a portal to another world. Defeat the Ender Dragon, and claim
    victory!
    """
    game: str = "Monster Hunter Frontier"
    option_definitions = minecraft_options
    settings: typing.ClassVar[MHFSettings]
    topology_present = True
    web = MinecraftWebWorld()

    item_name_to_id = Constants.item_name_to_id
    location_name_to_id = Constants.location_name_to_id

    def _get_mc_data(self) -> Dict[str, Any]:
        return {
            'world_seed': self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            'seed_name': self.multiworld.seed_name,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'death_link': bool(self.multiworld.death_link[self.player].value),
            'starting_items': str(self.multiworld.starting_items[self.player].value),
            'include_unfair_quests': bool(self.multiworld.include_unfair_quests[self.player].value),
            'race': self.multiworld.is_race,
        }

    def create_item(self, name: str) -> Item:
        item_class = ItemClassification.filler
        if name in Constants.item_info["progression_items"]:
            item_class = ItemClassification.progression
        elif name in Constants.item_info["useful_items"]:
            item_class = ItemClassification.useful
        elif name in Constants.item_info["trap_items"]:
            item_class = ItemClassification.trap

        return MHFItem(name, item_class, self.item_name_to_id.get(name, None), self.player)

    def create_event(self, region_name: str, event_name: str) -> None:
        region = self.multiworld.get_region(region_name, self.player)
        loc = MHFLocation(self.player, event_name, None, region)
        loc.place_locked_item(self.create_event_item(event_name))
        region.locations.append(loc)

    def create_event_item(self, name: str) -> None:
        item = self.create_item(name)
        item.classification = ItemClassification.progression
        return MHFItem(name, item.classification, None, self.player)

    def create_regions(self) -> None:
        self.multiworld.regions += [
            create_region(self.multiworld, self.player, 'Menu', None, ['Overworld Entrance']),
            create_region(self.multiworld, self.player, 'Overworld', self.location_name_to_id, ['HR 1 Gate']),
            create_region(self.multiworld, self.player, 'HR 1', None, ['HR 2 Gate']),
            create_region(self.multiworld, self.player, 'HR 2', None, ['HR 3 Gate']),
            create_region(self.multiworld, self.player, 'HR 3', None, ['HR 4 Gate']),
            create_region(self.multiworld, self.player, 'HR 4', None, ['HR 5 Gate']),
            create_region(self.multiworld, self.player, 'HR 5', None, ['HR 6 Gate']),
            create_region(self.multiworld, self.player, 'HR 6', None, []),
        ]

        # link up our region with the entrance we just made
        self.multiworld.get_entrance('Overworld Entrance', self.player)\
            .connect(self.multiworld.get_region('Overworld', self.player))
        
        self.multiworld.get_entrance('HR 1 Gate', self.player)\
            .connect(self.multiworld.get_region('HR 1', self.player))
        
        self.multiworld.get_entrance('HR 2 Gate', self.player)\
            .connect(self.multiworld.get_region('HR 2', self.player))
        
        self.multiworld.get_entrance('HR 3 Gate', self.player)\
            .connect(self.multiworld.get_region('HR 3', self.player))
        
        self.multiworld.get_entrance('HR 4 Gate', self.player)\
            .connect(self.multiworld.get_region('HR 4', self.player))
        
        self.multiworld.get_entrance('HR 5 Gate', self.player)\
            .connect(self.multiworld.get_region('HR 5', self.player))
        
        self.multiworld.get_entrance('HR 6 Gate', self.player)\
            .connect(self.multiworld.get_region('HR 6', self.player))
        
        # self.create_event('HR 7', 'Star Guildie Badge')

    def create_items(self) -> None:
        self.multiworld.itempool += build_item_pool(self)

    set_rules = set_rules

    def generate_output(self, output_directory: str) -> None:
        data = self._get_mc_data()
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apmhf"
        with open(os.path.join(output_directory, filename), 'wb') as f:
            f.write(b64encode(bytes(json.dumps(data), 'utf-8')))

    def fill_slot_data(self) -> dict:
        slot_data = self._get_mc_data()
        for option_name in minecraft_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def get_filler_item_name(self) -> str:
        return get_junk_item_names(self.multiworld.random, 1)[0]

def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    region = Region(name, player, world)
    if locations:
        for location_name in locations.keys():
            location = MHFLocation(player, location_name, locations[location_name], region)
            region.locations.append(location)

    if exits:
        for _exit in exits:
            region.exits.append(Entrance(player, _exit, region))

    return region

class MHFLocation(Location):
    game = "Monster Hunter Frontier"

class MHFItem(Item):
    game = "Monster Hunter Frontier"
