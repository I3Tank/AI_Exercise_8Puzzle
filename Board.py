# the coordinates for our board
coord_list = [(0, 0), (1, 0), (2, 0),
              (0, 1), (1, 1), (2, 1),
              (0, 2), (1, 2), (2, 2)]

empty_tile_coord = [0, 0]

# goal State
goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
current_state = []


def get_goal_state():
    return goal_state


def get_current_state():
    return current_state


def get_coord_list():
    return coord_list


def get_empty_coord():
    return empty_tile_coord


def update_empty_coord(new_coord):
    empty_tile_coord[0] = new_coord[0]
    empty_tile_coord[1] = new_coord[1]
