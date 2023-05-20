import csv
import enum
from dataclasses import dataclass
from random import Random
from typing import Optional, Dict, Protocol, List, FrozenSet

from . import options, data

LOCATION_CODE_OFFSET = 717000


class LocationTags(enum.Enum):
    MANDATORY = enum.auto()
    QUESTS = enum.auto()
    SKILL_LEVEL = enum.auto()
    BOSSES = enum.auto()


@dataclass(frozen=True)
class LocationData:
    code_without_offset: Optional[int]
    region: str
    name: str
    tags: FrozenSet[LocationTags] = frozenset()

    @property
    def code(self) -> Optional[int]:
        return LOCATION_CODE_OFFSET + self.code_without_offset if self.code_without_offset is not None else None


class BL2LocationCollector(Protocol):
    def __call__(self, name: str, code: Optional[int], region: str) -> None:
        raise NotImplementedError


def load_location_csv() -> List[LocationData]:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files

    with files(data).joinpath("locations.csv").open() as file:
        reader = csv.DictReader(file)
        return [LocationData(int(location["id"]) if location["id"] else None,
                             location["region"],
                             location["name"],
                             frozenset(LocationTags[group]
                                       for group in location["tags"].split(",")
                                       if group))
                for location in reader]


events_locations = [
    LocationData(None, "Borderlands 2", "Complete the main story"),
]

all_locations = load_location_csv() + events_locations
location_table: Dict[str, LocationData] = {location.name: location for location in all_locations}
locations_by_tag: Dict[LocationTags, List[LocationData]] = {}


def initialize_groups():
    for location in all_locations:
        for tag in location.tags:
            location_group = locations_by_tag.get(tag, list())
            location_group.append(location)
            locations_by_tag[tag] = location_group


initialize_groups()

def create_locations(location_collector: BL2LocationCollector,
                     world_options: options.StardewOptions,
                     random: Random):
    randomized_locations = []

    randomized_locations.extend(locations_by_tag[LocationTags.MANDATORY])

    if not world_options[options.SkillProgression] == options.SkillProgression.option_vanilla:
        randomized_locations.extend(locations_by_tag[LocationTags.SKILL_LEVEL])

    for location_data in randomized_locations:
        location_collector(location_data.name, location_data.code, location_data.region)
