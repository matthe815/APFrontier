from math import ceil
from typing import List

from BaseClasses import MultiWorld, Item
from worlds.AutoWorld import World

from . import Constants

def get_junk_item_names(rand, k: int) -> str:
	junk_weights = Constants.item_info["junk_weights"]
	junk = rand.choices(
		list(junk_weights.keys()),
		weights=list(junk_weights.values()),
		k=k)
	return junk

def build_item_pool(mc_world: World) -> List[Item]:
	multiworld = mc_world.multiworld
	player = mc_world.player

	itempool = []
	total_location_count = len(multiworld.get_unfilled_locations(player))
	print(f"Total locations: {total_location_count}")

	required_pool = Constants.item_info["required_pool"]
	junk_weights = Constants.item_info["junk_weights"]

	# Add required progression items
	for item_name, num in required_pool.items():
		itempool += [mc_world.create_item(item_name) for _ in range(num)]

	# Fill remaining itempool with randomly generated junk
	junk = get_junk_item_names(multiworld.random, (total_location_count - len(itempool)) * 2)
	itempool += [mc_world.create_item(name) for name in junk]

	print(f"Item pool size: {len(itempool)}")

	return itempool
