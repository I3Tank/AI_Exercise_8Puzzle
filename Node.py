class Node:
    parent = None
    game_state = []
    empty_tile_coordinate = (0, 0)
    # moves
    g = 0
    # heuristic
    h = 0
    # f = g + h
    f = 0

    def __init__(self, parent, game_state, empty_tile_coordinate, g, h):
        self.parent = parent
        self.game_state = game_state
        self.empty_tile_coordinate = empty_tile_coordinate
        self.g = g
        self.h = h
        self.f = g + h
