from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule

def set_rules(world: MultiWorld, player: int):
    for i in range(2, 10):
        set_rule(world.get_location(f"Chessipelago Level {i} - Objective 1", player), lambda state: state.has(f'Level {i}', player))
        set_rule(world.get_location(f"Chessipelago Level {i} - Objective 2", player), lambda state: state.has(f'Level {i}', player))
        set_rule(world.get_location(f"Chessipelago Level {i} - Objective 3", player), lambda state: state.has(f'Level {i}', player))
        set_rule(world.get_location(f"Chessipelago Level {i} - Objective 4", player), lambda state: state.has(f'Level {i}', player))

    world.completion_condition[player] =\
        lambda state:\
        state.can_reach(world.get_location("Chessipelago Level 10 - Objective 1", player), "Location", player)
