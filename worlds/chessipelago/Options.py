import typing
from Options import Option, Toggle, DeathLink

class Piece_Randomizer(Toggle): 
    """The piece randomization settings"""
    display_name = "Randomize Pieces"

class OopsAllTraps(Toggle):
    """Makes all non-progression items traps."""
    display_name = "Oops All Traps"

chessipelago_options: typing.Dict[str, type(Option)] = {
    "piece_randomizer": Piece_Randomizer, 
    "oops_all_traps": OopsAllTraps,
    "death_link": DeathLink,
}
