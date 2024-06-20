import typing
from Options import Choice, Option, Toggle, DefaultOnToggle, Range, OptionList, DeathLink, PlandoConnections

class StartingItems(OptionList):
    """Start with these items. Each entry should be of this format: {item: "item_name", amount: #, nbt: "nbt_string"}"""
    display_name = "Starting Items"

class UnfairQuests(Toggle):
    """Include unfair quests in the quest pool."""
    display_name = "Include Unfair Quests"


minecraft_options: typing.Dict[str, type(Option)] = {
    "death_link":                           DeathLink,
    "starting_items":                       StartingItems,
    "include_unfair_quests":                UnfairQuests,
}
