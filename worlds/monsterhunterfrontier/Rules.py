import typing
from collections.abc import Callable

from BaseClasses import CollectionState
from worlds.generic.Rules import exclusion_rules
from worlds.AutoWorld import World

from . import Constants

# Helper functions
# moved from logicmixin
def can_access_hr2(state: CollectionState, player: int) -> bool:
    return state.has('HR 1 Urgent Quest Ticket', player)

def can_access_hr3(state: CollectionState, player: int) -> bool:
    return can_access_hr2(state, player) and state.has('HR 2 Urgent Quest Ticket', player)

def can_access_hr4(state: CollectionState, player: int) -> bool:
    return can_access_hr3(state, player) and state.has('HR 3 Urgent Quest Ticket', player)

def can_access_hr5(state: CollectionState, player: int) -> bool:
    return can_access_hr4(state, player) and state.has('HR 4 Urgent Quest Ticket', player)

def can_access_hr6(state: CollectionState, player: int) -> bool:
    return can_access_hr5(state, player) and state.has('HR 5 Urgent Quest Ticket', player)

def can_access_hr7(state: CollectionState, player: int) -> bool:
    return can_access_hr6(state, player), state.has('HR 6 Urgent Quest Ticket', player)


def get_rules_lookup(player: int):
    rules_lookup: typing.Dict[str, typing.List[Callable[[CollectionState], bool]]] = {
        "entrances": {
            "HR 1 Gate": lambda state: True,
            "HR 2 Gate": lambda state: can_access_hr2(state, player),
            "HR 3 Gate": lambda state: can_access_hr3(state, player),
            "HR 4 Gate": lambda state: can_access_hr4(state, player),
            "HR 5 Gate": lambda state: can_access_hr5(state, player),
            "HR 6 Gate": lambda state: can_access_hr6(state, player)
        },
        "locations": {
            "HR 1 - Quest 1": lambda state: True,
            "HR 1 - Quest 2": lambda state: True,
            "HR 1 - Quest 3": lambda state: True,
            "HR 1 - Quest 4": lambda state: True,
            "HR 1 - Quest 5": lambda state: True,
            "HR 1 - Quest 6": lambda state: True,
            "HR 1 - Urgent": lambda state: state.has("HR 1 Urgent Quest Ticket", player),
            "HR 2 - Quest 1": lambda state: can_access_hr2(state, player),
            "HR 2 - Quest 2": lambda state: can_access_hr2(state, player),
            "HR 2 - Quest 3": lambda state: can_access_hr2(state, player),
            "HR 2 - Quest 4": lambda state: can_access_hr2(state, player),
            "HR 2 - Quest 5": lambda state: can_access_hr2(state, player),
            "HR 2 - Quest 6": lambda state: can_access_hr2(state, player),
            "HR 2 - Urgent": lambda state: can_access_hr2(state, player) and state.has('HR 2 Urgent Quest Ticket', player),
            "HR 3 - Quest 1": lambda state: can_access_hr3(state, player),
            "HR 3 - Quest 2": lambda state: can_access_hr3(state, player),
            "HR 3 - Quest 3": lambda state: can_access_hr3(state, player),
            "HR 3 - Quest 4": lambda state: can_access_hr3(state, player),
            "HR 3 - Quest 5": lambda state: can_access_hr3(state, player),
            "HR 3 - Quest 6": lambda state: can_access_hr3(state, player),
            "HR 3 - Urgent": lambda state: can_access_hr3(state, player) and state.has('HR 3 Urgent Quest Ticket', player),
            "HR 4 - Quest 1": lambda state: can_access_hr4(state, player),
            "HR 4 - Quest 2": lambda state: can_access_hr4(state, player),
            "HR 4 - Quest 3": lambda state: can_access_hr4(state, player),
            "HR 4 - Quest 4": lambda state: can_access_hr4(state, player),
            "HR 4 - Quest 5": lambda state: can_access_hr4(state, player),
            "HR 4 - Quest 6": lambda state: can_access_hr4(state, player),  
            "HR 4 - Urgent": lambda state: can_access_hr4(state, player) and state.has('HR 4 Urgent Quest Ticket', player),
            "HR 5 - Quest 1": lambda state: can_access_hr5(state, player),
            "HR 5 - Quest 2": lambda state: can_access_hr5(state, player),
            "HR 5 - Quest 3": lambda state: can_access_hr5(state, player),
            "HR 5 - Quest 4": lambda state: can_access_hr5(state, player),
            "HR 5 - Quest 5": lambda state: can_access_hr5(state, player),
            "HR 5 - Quest 6": lambda state: can_access_hr5(state, player),
            "HR 5 - Urgent": lambda state: can_access_hr5(state, player) and state.has('HR 5 Urgent Quest Ticket', player),
            "HR 6 - Quest 1": lambda state: can_access_hr6(state, player),
            "HR 6 - Quest 2": lambda state: can_access_hr6(state, player),
            "HR 6 - Quest 3": lambda state: can_access_hr6(state, player),
            "HR 6 - Quest 4": lambda state: can_access_hr6(state, player),
            "HR 6 - Quest 5": lambda state: can_access_hr6(state, player),
            "HR 6 - Quest 6": lambda state: can_access_hr6(state, player),
            "HR 6 - Urgent": lambda state: can_access_hr6(state, player)
        }
    }
    return rules_lookup


def set_rules(mc_world: World) -> None:
    multiworld = mc_world.multiworld
    player = mc_world.player

    rules_lookup = get_rules_lookup(player)

    # Set entrance rules
    for entrance_name, rule in rules_lookup["entrances"].items():
        multiworld.get_entrance(entrance_name, player).access_rule = rule

    # Set location rules
    for location_name, rule in rules_lookup["locations"].items():
        multiworld.get_location(location_name, player).access_rule = rule

    completion_requirements = lambda state: can_access_hr7(state, player) and state.has('Star Guildie Badge', player)
    multiworld.completion_condition[player] = lambda state: completion_requirements(state)
