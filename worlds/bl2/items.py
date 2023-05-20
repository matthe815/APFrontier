import bisect
import csv
import enum
import itertools
import logging
import math
import typing
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from random import Random
from typing import Dict, List, Protocol, Union, Set, Optional, FrozenSet

from BaseClasses import Item, ItemClassification

ITEM_CODE_OFFSET = 717000

logger = logging.getLogger(__name__)
world_folder = Path(__file__).parent


class Group(enum.Enum):
    GUN = enum.auto()
    GRENADE = enum.auto()
    SHIELD = enum.auto()
    CLASS_MOD = enum.auto() 

    SKILL_LEVEL_UP = enum.auto()

@dataclass(frozen=True)
class ItemData:
    code_without_offset: Optional[int]
    name: str
    classification: ItemClassification
    groups: Set[Group] = field(default_factory=frozenset)

    def __post_init__(self):
        if not isinstance(self.groups, frozenset):
            super().__setattr__("groups", frozenset(self.groups))

    @property
    def code(self):
        return ITEM_CODE_OFFSET + self.code_without_offset if self.code_without_offset is not None else None

    def has_any_group(self, *group: Group) -> bool:
        groups = set(group)
        return bool(groups.intersection(self.groups))
    
class BL2ItemFactory(Protocol):
    def __call__(self, name: Union[str, ItemData]) -> Item:
        raise NotImplementedError
    
def load_item_csv():
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # noqa

    items = []
    with files(data).joinpath("items.csv").open() as file:
        item_reader = csv.DictReader(file)
        for item in item_reader:
            id = int(item["id"]) if item["id"] else None
            classification = ItemClassification[item["classification"]]
            groups = {Group[group] for group in item["groups"].split(",") if group}
            items.append(ItemData(id, item["name"], classification, groups))
    return items

events = [
    ItemData(None, "Victory", ItemClassification.progression),
]

all_items: List[ItemData] = load_item_csv() + events

item_table: Dict[str, ItemData] = {}
items_by_group: Dict[Group, List[ItemData]] = {}

def initialize_groups():
    for item in all_items:
        for group in item.groups:
            item_group = items_by_group.get(group, list())
            item_group.append(item)
            items_by_group[group] = item_group


def initialize_item_table():
    item_table.update({item.name: item for item in all_items})

initialize_item_table()
initialize_groups()

def create_items(item_factory: BL2ItemFactory, locations_count: int, items_to_exclude: List[Item], world_options: StardewOptions,
                 random: Random) -> List[Item]:
    items = create_unique_items(item_factory, world_options, random)

    for item in items_to_exclude:
        if item in items:
            items.remove(item)

    assert len(items) <= locations_count, \
        "There should be at least as many locations as there are mandatory items"
    logger.debug(f"Created {len(items)} unique items")

    gun_filler_items = fill_with_guns(item_factory, world_options, random, locations_count - len(items))
    items += gun_filler_items
    logger.debug(f"Created {len(gun_filler_items)} resource packs")

    return items

def create_unique_items(item_factory: BL2ItemFactory, world_options: StardewOptions, random: Random) -> List[Item]:
    items = []

    return items

def fill_with_guns(item_factory: BL2ItemFactory, world_options: options.StardewOptions, random: Random,
                             required_guns: int) -> List[Item]:
    items = []

    for i in range(required_guns):
        # create guns
        print("Creating gun")

    return items