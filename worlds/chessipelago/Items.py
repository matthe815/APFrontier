from BaseClasses import ItemClassification

class ItemData:
    def __init__(self, id, count, classification, groups):
        self.groups = groups
        self.count = count
        self.classification = classification
        self.id = None if id is None else id + 172000000

item_table = {
    'Queen': ItemData(1, 1, ItemClassification.useful, ["Pieces"]),
    'Bishop': ItemData(2, 4, ItemClassification.useful, ["Pieces"]),
    'Rook': ItemData(3, 4, ItemClassification.useful, ["Pieces"]),
    'Knight': ItemData(3, 4, ItemClassification.useful, ["Pieces"]),
    'Pawn': ItemData(4, 12, ItemClassification.useful, ["Pieces"]),
    'Level 2': ItemData(5, 1, ItemClassification.progression, ["Levels"]),
    'Level 3': ItemData(6, 1, ItemClassification.progression, ["Levels"]),
    'Level 4': ItemData(7, 1, ItemClassification.progression, ["Levels"]),
    'Level 5': ItemData(8, 1, ItemClassification.progression, ["Levels"]),
    'Level 6': ItemData(9, 1, ItemClassification.progression, ["Levels"]),
    'Level 7': ItemData(10, 1, ItemClassification.progression, ["Levels"]),
    'Level 8': ItemData(11, 1, ItemClassification.progression, ["Levels"]),
    'Level 9': ItemData(12, 1, ItemClassification.progression, ["Levels"]),
    'Level 10': ItemData(13, 1,  ItemClassification.progression, ["Levels"]),
    'Promotions': ItemData(14, 1, ItemClassification.useful, ["Levels"]),
    'Teleport Trap': ItemData(15, 1, ItemClassification.trap, ["Traps"]),
    'Piece Change Trap': ItemData(16, 1, ItemClassification.trap, ["Traps"]),
    'Rewind': ItemData(17, 4, ItemClassification.filler, ["Filler"])
}
