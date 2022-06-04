import Board
from Helper import Helper
from Heuristic import Heuristic
from Node import Node
from time import perf_counter

# solve mode 0 = misplaced tiles, 1 = manhattan
solve_mode = 0
# open list is the list full of "visitable" nodes, closed list contains all already expanded nodes
open_list = []
closed_list = []


class AStar:
    @staticmethod
    def generate_child_nodes(parent_node):
        child_list = []
        current_game_state = parent_node.game_state

        # all possible moves based on the location of the empty tile
        coord_up = (parent_node.empty_tile_coordinate[0], parent_node.empty_tile_coordinate[1] - 1)
        coord_left = (parent_node.empty_tile_coordinate[0] - 1, parent_node.empty_tile_coordinate[1])
        coord_down = (parent_node.empty_tile_coordinate[0], parent_node.empty_tile_coordinate[1] + 1)
        coord_right = (parent_node.empty_tile_coordinate[0] + 1, parent_node.empty_tile_coordinate[1])

        def try_move_to(coordinate):
            # check if the move is legal
            if Helper.check_if_coord_inside_board(coordinate):
                # calculate the new state
                block_number = Helper.get_block_number_by_coordinates(coordinate, current_game_state)
                new_state = current_game_state.copy()
                new_state = Helper.swap_numbers_in_state(0, block_number, new_state)
                # add the new node to the child list
                # solve using misplaces blocks
                if solve_mode == 0:
                    new_child = Node(parent_node, new_state, coordinate, parent_node.g + 1, Heuristic.get_misplaced_block_count(new_state, Board.goal_state))
                # solve using manhattan distance
                elif solve_mode == 1:
                    new_child = Node(parent_node, new_state, coordinate, parent_node.g + 1, Heuristic.get_manhattan_distance(new_state, Board.goal_state))
                child_list.append(new_child)

        # try all possible moves
        try_move_to(coord_up)
        try_move_to(coord_left)
        try_move_to(coord_down)
        try_move_to(coord_right)

        return child_list

    @staticmethod
    def a_star():
        reached_goal = False

        # while the list is not empty
        while len(open_list) > 0 and not reached_goal:
            # select the node with the smallest f value and remove it from the open list
            current_node = open_list[len(open_list) - 1]
            # print(current_node.f)
            open_list.pop()
            # generate children of this node
            # we only check the newly created nodes if they are the goal state or already in open/closed since all others
            # already have been checked
            child_list = AStar.generate_child_nodes(current_node)
            # now we have all new nodes in the child_list
            for child in child_list:
                # if the child is the goal, stop searching
                if child.game_state == Board.get_goal_state():
                    reached_goal = True
                    goal_node = child
                    break
                # else add it to the open list
                else:
                    # check if node with same game state is in closed list, if f is higher -> skip it
                    # if the node with the same game state is already in open list but has higher f -> skip it
                    if AStar.check_if_in_open_list(child) and AStar.check_if_in_closed_list(child):
                        AStar.add_node_to_open_list(child)

            # at the end add the current node to the closed list
            closed_list.append(current_node)
        print("Algorithm finished!")
        step_list = []
        # here we go up the tree through the parents and reverse the direction
        while goal_node.parent is not None:
            step_list.append(goal_node)
            goal_node = goal_node.parent
        step_list.append(goal_node)
        step_list.reverse()

        AStar.print_statistics(step_list)

    @staticmethod
    def solve_using_a_star():
        start_state = Board.current_state
        # clear the lists for the other algorithm
        closed_list.clear()
        open_list.clear()

        # create the first node and add it to the open list
        start_node = Node(None, start_state, Board.get_empty_coord(), 0, 0)
        AStar.add_node_to_open_list(start_node)

        AStar.a_star()

    @staticmethod
    def check_if_in_open_list(node_to_check):
        result = True
        for node in open_list:
            # if the state is identical to one in the open list and the f node is higher -> skip it
            if node.game_state == node_to_check.game_state and node.f < node_to_check.f:
                result = False
                break
        return result

    @staticmethod
    def check_if_in_closed_list(node_to_check):
        result = True
        for node in closed_list:
            # if the state is identical to one in the closed list and the f node is higher -> skip it
            if node.game_state == node_to_check.game_state and node.f < node_to_check.f:
                result = False
        return result

    @staticmethod
    def add_node_to_open_list(new_node):
        # if the list is empty, add it
        open_list.append(new_node)
        # then sort the list so the node with the smallest f and the highest g is at the end of the open list
        open_list.sort(key=lambda x: (x.f, -x.g), reverse=True)

    @staticmethod
    def solve_using_manhattan_distance():
        global solve_mode
        solve_mode = 1
        AStar.solve_using_a_star()

    @staticmethod
    def solve_using_misplaced_tiles():
        global solve_mode
        solve_mode = 0
        AStar.solve_using_a_star()

    @staticmethod
    def compare_heuristics():
        t1_start = perf_counter()
        print("Started solving with manhattan distance")
        AStar.solve_using_manhattan_distance()
        t1_stop = perf_counter()
        print("Elapsed time for manhattan: %.4f s" % (t1_stop - t1_start))
        print("Started solving with misplaced tiles")
        AStar.solve_using_misplaced_tiles()
        t2_stop = perf_counter()
        print("Elapsed time for misplaced tiles: %.4f s" % (t2_stop - t1_stop))

    @staticmethod
    def print_statistics(step_list):
        for step in step_list:
            print(str(step.g) + " : " + str(step.game_state))

        print("Number of expanded nodes:  " + str(len(closed_list)))
        print("Steps needed: " + str(len(step_list)))


