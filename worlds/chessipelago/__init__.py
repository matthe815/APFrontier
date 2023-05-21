from BaseClasses import Item, MultiWorld, Region, Location, Entrance, Tutorial, ItemClassification
from .Items import item_table
from .Rules import set_rules
from .Options import chessipelago_options
from ..AutoWorld import World, WebWorld
from datetime import datetime


class ChessipelagoWebWorld(WebWorld):
    theme = 'partyTime'
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to playing Chessipelago',
            language='English',
            file_name='guide_en.md',
            link='guide/en',
            authors=['Farrak Kilhn']
        ),
        Tutorial(
            tutorial_name='Guide d installation',
            description='Un guide pour jouer à Chessipelago',
            language='Français',
            file_name='guide_fr.md',
            link='guide/fr',
            authors=['TheLynk']
        )
    ]


class ChessipelagoWorld(World):
    """
    A chess game for Archipelago; Play chess. Get items.
    """
    game = "Chessipelago"
    topology_present = False
    data_version = 5
    option_definitions: dict = chessipelago_options
    web = ChessipelagoWebWorld()

    item_name_to_id = {}
    start_id = 9000
    
    for item in item_table:
        item_name_to_id[item] = start_id
        start_id += 1
        print(f"{item}: {item_name_to_id[item]}")

    location_name_to_id = {}
    start_id = 9000

    for i in range(1, 11):
        location_name_to_id[f"Chessipelago Level {i} - Objective 1"] = start_id
        start_id += 1
        location_name_to_id[f"Chessipelago Level {i} - Objective 2"] = start_id
        start_id += 1
        location_name_to_id[f"Chessipelago Level {i} - Objective 3"] = start_id
        start_id += 1
        location_name_to_id[f"Chessipelago Level {i} - Objective 4"] = start_id
        start_id += 1

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_item(self, name: str, classification: ItemClassification) -> Item:
        return Item(name, classification, self.item_name_to_id[name], self.player)

    def create_items(self):
        item_table_copy = list(item_table)
        self.multiworld.random.shuffle(item_table_copy)

        item_pool = []

        for i in range(len(item_table_copy)):
            item = ChessipelagoItem(
                item_table_copy[i],
                ItemClassification.progression,
                self.item_name_to_id[item_table_copy[i]],
                self.player
            )

            for i in range(item_table[item_table_copy[i]].count):
                item_pool.append(item)

        self.multiworld.itempool += item_pool

    def create_regions(self):
        self.multiworld.regions += [
            create_region(self.multiworld, self.player, 'Menu', None, ['Menu']),
            create_region(self.multiworld, self.player, 'Game', self.location_name_to_id)
        ]

        # link up our region with the entrance we just made
        self.multiworld.get_entrance('Menu', self.player)\
            .connect(self.multiworld.get_region('Game', self.player))
            
    def get_filler_item_name(self) -> str:
        return item_table["Rewind"]


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    region = Region(name, player, world)
    if locations:
        for location_name in locations.keys():
            location = ChessipelagoLocation(player, location_name, locations[location_name], region)
            region.locations.append(location)

    if exits:
        for _exit in exits:
            region.exits.append(Entrance(player, _exit, region))

    return region


class ChessipelagoItem(Item):
    game = "Chessipelago"


class ChessipelagoLocation(Location):
    game: str = "Chessipelago"
