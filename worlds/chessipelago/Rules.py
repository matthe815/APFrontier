from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class ChessipelagoLogic(LogicMixin):
    def _archipidle_location_is_accessible(self, player_id, items_required):
        items_received = 0
        for item in self.prog_items:
            if item[1] == player_id:
                items_received += 1

        return items_received >= items_required


def set_rules(world: MultiWorld, player: int):
    for i in range(1, 10):
        set_rule(
            world.get_location(f"Chessipelago Level {i}", player),
            lambda state: state.has(f'Chessipelago Level {i}', player)
        )

    world.completion_condition[player] =\
        lambda state:\
        state.can_reach(world.get_location("Chessipelago Level 10", player), "Location", player)
