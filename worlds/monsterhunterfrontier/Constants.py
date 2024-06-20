import os
import json
import pkgutil

def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)
    return json.loads(pkgutil.get_data(__name__, fname).decode())

# For historical reasons, these values are different.
# They remain different to ensure datapackage consistency.
# Do not separate other games' location and item IDs like this.
item_id_offset: int 	= 45000
location_id_offset: int = 5135230

item_info = load_data_file("items.json")
item_name_to_id = {name: item_id_offset + index \
	for index, name in enumerate(item_info["all_items"])}
# item_name_to_id["Bee Trap"] = item_id_offset + 100  # historical reasons

location_info = load_data_file("locations.json")

hr1 = location_info["HR 1"]
hr2 = location_info["HR 2"]
hr3 = location_info["HR 3"]
hr4 = location_info["HR 4"]
hr5 = location_info["HR 5"]
hr6 = location_info["HR 6"]

all_hrs = hr1 + hr2 + hr3 + hr4 + hr5 + hr6

location_name_to_id = {name: location_id_offset + index \
	for index, name in enumerate(all_hrs)}

exclusion_info = load_data_file("excluded_locations.json")
