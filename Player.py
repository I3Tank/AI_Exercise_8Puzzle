import Board
from Helper import Helper


class Player:

    @staticmethod
    def move_to_empty_box(empty_box_coord, block_to_move):
        block_to_move.button_ref.master.grid(row=empty_box_coord[1], column=empty_box_coord[0])
        Helper.swap_numbers_in_state(block_to_move.number, 0, Board.current_state)
        Board.update_empty_coord(block_to_move.coordinate)

    @staticmethod
    def check_adjacent_tiles(block):
        current_coord = block.coordinate

        # coordinates to check Up, Down, Left, Right
        coord_to_check_up = (current_coord[0], current_coord[1] - 1)
        coord_to_check_down = (current_coord[0], current_coord[1] + 1)
        coord_to_check_left = (current_coord[0] - 1, current_coord[1])
        coord_to_check_right = (current_coord[0] + 1, current_coord[1])

        def try_move(coordinate):
            # check if the move is legal and if it is the empty block
            if Helper.check_if_coord_inside_board(coordinate) and coordinate == tuple(Board.get_empty_coord()):
                # move the block and update its coordinates
                Player.move_to_empty_box(coordinate, block)
                block.coordinate = coordinate

        # try all possible moves
        try_move(coord_to_check_up)
        try_move(coord_to_check_left)
        try_move(coord_to_check_down)
        try_move(coord_to_check_right)

    @staticmethod
    def on_button_click(event, block):
        Player.check_adjacent_tiles(block)
