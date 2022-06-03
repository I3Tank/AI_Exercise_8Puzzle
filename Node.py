class Node:
    parent = None
    current_game_state = []
    empty_tile_coordinate = (0, 0)
    # moves
    g = 0
    # heuristic
    h = 0
    # f = g + h
    f = 0

    def __init__(self, parent, current_game_state, empty_tile_coordinate, g, h):
        self.parent = parent
        self.current_game_state = current_game_state
        self.empty_tile_coordinate = empty_tile_coordinate
        self.g = g
        self.h = h
        self.f = g + h
