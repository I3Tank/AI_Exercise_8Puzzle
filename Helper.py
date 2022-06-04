# our class for the various checks that we need
import Board


class Helper:
    @staticmethod
    def check_if_coord_inside_board(coord_to_check):
        if 0 <= coord_to_check[0] <= 2 and 0 <= coord_to_check[1] <= 2:
            return True

    @staticmethod
    def check_if_solvable(game_state):
        steps = len(game_state)
        inversion_counter = 0
        # i = number currently looking at
        for i in range(steps):
            # j = numbers that come after i
            for j in range(i + 1, steps):
                if game_state[i] > game_state[j] and not 0:
                    inversion_counter += 1
        print("inv_count: " + str(inversion_counter))

        # the puzzle is solvable if the inversion counter is even
        if inversion_counter % 2 == 0:
            return True
        else:
            return False

    @staticmethod
    # swap two numbers inside a game state (list)
    def swap_numbers_in_state(a, b, list_to_swap):
        index_a = list_to_swap.index(a)
        index_b = list_to_swap.index(b)

        list_to_swap[index_a] = b
        list_to_swap[index_b] = a

        return list_to_swap

    @staticmethod
    def get_block_number_by_coordinates(coordinates, game_state):
        index = Board.get_coord_list().index(coordinates)
        return game_state[index]
