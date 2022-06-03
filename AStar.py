import operator

import Board
from Helper import Helper
from Heuristic import Heuristic
from Node import Node


class AStar:

    open_list = []
    closed_list = []

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
                block_number = Helper.get_block_number_by_coordinates(coordinate)
                new_state = current_game_state.copy()
                new_state = Helper.swap_numbers_in_state(0, block_number, new_state)
                # add the new node to the child list
                new_child = Node(parent_node, new_state, coordinate, parent_node.g + 1, Heuristic.get_misplaced_block_count(new_state, Board.goal_state))
                child_list.append(new_child)

        # try all possible moves
        try_move_to(coord_up)
        try_move_to(coord_left)
        try_move_to(coord_down)
        try_move_to(coord_right)

        return child_list

    @staticmethod
    def a_star(open_list=open_list):
        reached_goal = False

        # while the list is not empty
        while len(open_list) > 0 and not reached_goal:
            # select the current node and remove it from the open list
            current_node = open_list[len(open_list) - 1]
            print(current_node.game_state)
            open_list.pop()
            # generate children of this node
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
                    # print("openlist: " + str(check_if_already_in_open_list(child)) + "  closedlist: " + str(check_if_in_closed_list(child)))
                    if AStar.check_if_in_open_list(child) and AStar.check_if_in_closed_list(child):
                        AStar.add_node_to_open_list(child)

            # at the end add the current node to the closed list
            AStar.closed_list.append(current_node)
            # print("Step: " + str(current_node.g))
            # cnt = 0
            # for x in open_list:
            #     print(str(cnt) + ": " + str(x.f))
            #     cnt += 1
        print("solved?")
        while goal_node.parent is not None:
            print(str(goal_node.g) + " : " + str(goal_node.game_state))
            goal_node = goal_node.parent

    @staticmethod
    def solve_using_a_star():
        start_state = Board.current_state
        # create the first node and add it to the open list
        start_node = Node(None, start_state, Board.get_empty_coord(), 0, 0)
        AStar.add_node_to_open_list(start_node)

        AStar.a_star()

    @staticmethod
    def check_if_in_open_list(node_to_check):
        node_to_remove = None
        result = True
        for node in AStar.open_list:
            if node.game_state == node_to_check.game_state and node.f < node_to_check.f:
                # removing nodes without adding any if closed_list_check doesn't pass
                # node_to_remove = node
                result = False
                break
        if node_to_remove is not None:
            AStar.open_list.remove(node_to_remove)
        return result

    @staticmethod
    def check_if_in_closed_list(node_to_check):
        result = True
        for node in AStar.closed_list:
            if node.game_state == node_to_check.game_state and node.f < node_to_check.f:
                result = False
        return result

    @staticmethod
    def add_node_to_open_list(new_node):
        # if the list is empty, add it
        if len(AStar.open_list) == 0:
            AStar.open_list.append(new_node)
        else:
            AStar.open_list.append(new_node)
            AStar.open_list.sort(key=operator.attrgetter('f'), reverse=True)
