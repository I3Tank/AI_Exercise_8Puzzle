import Board as Board


# in this class we have the two heuristics needed
class Heuristic:
    # static method to check the misplaced blocks
    @staticmethod
    def get_misplaced_block_count(state_to_check, goal_state):
        misplaced_blocks = 0

        for i in goal_state:
            if goal_state[i] != state_to_check[i]:
                misplaced_blocks += 1
        return misplaced_blocks - 1

    # static method to check the manhattan distance
    @staticmethod
    def get_manhattan_distance(current_state, goal_state):
        coord_list = Board.get_coord_list()
        sum_of_distances = 0

        for i in range(len(current_state)):
            # get the number of the current block
            block_number = current_state[i]
            # get the index for the goal state list
            index_of_block = goal_state.index(block_number)
            # get the coord where the block should be
            goal_coord_x = coord_list[index_of_block][0]
            goal_coord_y = coord_list[index_of_block][1]
            # get the coord where the block currently is
            current_coord_x = coord_list[i][0]
            current_coord_y = coord_list[i][1]
            # calculate the distance
            distance_x = abs(goal_coord_x - current_coord_x)
            distance_y = abs(goal_coord_y - current_coord_y)

            total_distance = distance_x + distance_y
            sum_of_distances += total_distance

        return sum_of_distances
