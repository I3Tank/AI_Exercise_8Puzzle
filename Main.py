# Needed for the GUI
import operator
import tkinter as tk
import tkinter.font as myFont
import random
from Block import Block
from Node import Node

window = tk.Tk()
window.title("8-Puzzle")
# Center window on startup
window.eval('tk::PlaceWindow . center')

buttonSize = 100
fontStyle = myFont.Font(size=20)

# create a 1x1 pixel to scale the buttons as squares
pixelVirtual = tk.PhotoImage(width=1, height=1)

# create a list with all button coordinates
buttonCoordList = []

block_list = []

empty_tile_coord = [0, 0]

# goal State
goal_state_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
goal_state_coord_list = [(goal_state_list[0], 0, 0),
                         (goal_state_list[1], 1, 0),
                         (goal_state_list[2], 2, 0),
                         (goal_state_list[3], 0, 1),
                         (goal_state_list[4], 1, 1),
                         (goal_state_list[5], 2, 1),
                         (goal_state_list[6], 0, 2),
                         (goal_state_list[7], 1, 2),
                         (goal_state_list[8], 2, 2)]
current_state_list = []

open_list = []
closed_list = []
g_counter = 0


def check_if_solvable():
    steps = len(current_state_list)
    inversion_counter = 0
    # i = number currently looking at
    for i in range(steps):
        # j = numbers that come after i
        for j in range(i + 1, steps):
            if current_state_list[i] > current_state_list[j] and not 0:
                inversion_counter += 1
    print("inv_count: " + str(inversion_counter))

    # the puzzle is solvable if the inversion counter is even
    if inversion_counter % 2 == 0:
        return True
    else:
        return False


def check_block_distances():
    sum_of_distances = 0
    for i in range(len(block_list)):
        number_to_check = block_list[i].number
        index_of_number_to_check = goal_state_list.index(number_to_check)
        goal_coord_x = goal_state_coord_list[index_of_number_to_check][1]
        goal_coord_y = goal_state_coord_list[index_of_number_to_check][2]

        current_coord_x = block_list[i].coordinate[0]
        current_coord_y = block_list[i].coordinate[1]

        distance_x = abs(goal_coord_x - current_coord_x)
        distance_y = abs(goal_coord_y - current_coord_y)

        total_distance = distance_x + distance_y
        # print(str(number_to_check) + ":distance = " + str(total_distance))
        sum_of_distances += total_distance
    # print(sum_of_distances)


def check_misplaced_blocks(state_to_check):
    misplaced_blocks = 0

    for i in goal_state_list:
        if goal_state_list[i] != state_to_check[i]:
            misplaced_blocks += 1
    return misplaced_blocks


def check_if_coord_inside_board(coord_to_check):
    if 0 <= coord_to_check[0] <= 2 and 0 <= coord_to_check[1] <= 2:
        return True


def check_if_empty_box(coord_to_check):
    if check_if_coord_inside_board(coord_to_check) and coord_to_check[0] == empty_tile_coord[0] and coord_to_check[1] == empty_tile_coord[1]:
        return True
    return False


def move_to_empty_box(empty_box_coord, block_to_move):
    block_to_move.button_ref.master.grid(row=empty_box_coord[1], column=empty_box_coord[0])
    swap_numbers_in_list(block_to_move.number, 0, current_state_list)


def swap_numbers_in_list(a, b, list_to_swap):
    index_a = list_to_swap.index(a)
    index_b = list_to_swap.index(b)

    list_to_swap[index_a] = b
    list_to_swap[index_b] = a

    return list_to_swap


def check_adjacent_tiles(block):
    current_coord = block.coordinate

    next_coord = (0, 0)
    moved = False

    # coordinates to check Up, Down, Left, Right
    coord_to_check_up = (current_coord[0], current_coord[1] - 1)
    coord_to_check_down = (current_coord[0], current_coord[1] + 1)
    coord_to_check_left = (current_coord[0] - 1, current_coord[1])
    coord_to_check_right = (current_coord[0] + 1, current_coord[1])

    if check_if_empty_box(coord_to_check_up):
        move_to_empty_box(coord_to_check_up, block)
        next_coord = coord_to_check_up
        moved = True

    elif check_if_empty_box(coord_to_check_down):
        move_to_empty_box(coord_to_check_down, block)
        next_coord = coord_to_check_down
        moved = True

    elif check_if_empty_box(coord_to_check_left):
        move_to_empty_box(coord_to_check_left, block)
        next_coord = coord_to_check_left
        moved = True

    elif check_if_empty_box(coord_to_check_right):
        move_to_empty_box(coord_to_check_right, block)
        next_coord = coord_to_check_right
        moved = True

    if moved:
        # remove the current coord after moving
        buttonCoordList.remove(current_coord)

        # add the new coord to the list
        buttonCoordList.append(next_coord)
        block.coordinate = next_coord

        update_empty_tile_coord(current_coord)


# print(current_state_list)


# logic for the event of a click
def handle_click(event, block):
    check_adjacent_tiles(block)
    # check_misplaced_blocks()
    check_block_distances()


def solve_using_a_star():
    start_state = current_state_list
    # create the first node and add it to the open list
    start_node = Node(None, start_state, empty_tile_coord, 0, 0)
    add_node_to_open_list(start_node)

    a_star()


def a_star():
    reached_goal = False

    # while the list is not empty
    while len(open_list) > 0 and not reached_goal:
        # select the current node and remove it from the open list
        current_node = open_list[len(open_list) - 1]
        print(current_node.current_game_state)
        open_list.pop()
        # generate children of this node
        child_list = generate_child_nodes(current_node)
        # now we have all new nodes in the child_list
        for child in child_list:
            # if the child is the goal, stop searching
            if child.current_game_state == goal_state_list:
                reached_goal = True
                goal_node = child
                break
            # else add it to the open list
            else:
                # check if node with same game state is in closed list, if f is higher -> skip it
                # if the node with the same game state is already in open list but has higher f -> skip it
                # print("openlist: " + str(check_if_already_in_open_list(child)) + "  closedlist: " + str(check_if_in_closed_list(child)))
                if check_if_already_in_open_list(child) and check_if_in_closed_list(child):
                    add_node_to_open_list(child)

        # at the end add the current node to the closed list
        closed_list.append(current_node)
        # print("Step: " + str(current_node.g))
        # cnt = 0
        # for x in open_list:
        #     print(str(cnt) + ": " + str(x.f))
        #     cnt += 1
    print("solved?")
    while goal_node.parent is not None:
        print(goal_node.current_game_state)
        goal_node = goal_node.parent


def check_if_already_in_open_list(node_to_check):
    node_to_remove = None
    result = True
    for node in open_list:
        if node.current_game_state == node_to_check.current_game_state and node.f < node_to_check.f:
            # removing nodes without adding any if closed_list_check doesn't pass
            # node_to_remove = node
            result = False
            break
    if node_to_remove is not None:
        open_list.remove(node_to_remove)
    return result


def check_if_in_closed_list(node_to_check):
    result = True
    for node in closed_list:
        if node.current_game_state == node_to_check.current_game_state and node.f < node_to_check.f:
            result = False
    return result


def generate_child_nodes(current_node):
    global g_counter
    g_counter += 1

    child_list = []
    current_game_state = current_node.current_game_state

    coord_up = (current_node.empty_tile_coordinate[0], current_node.empty_tile_coordinate[1] - 1)
    coord_left = (current_node.empty_tile_coordinate[0] - 1, current_node.empty_tile_coordinate[1])
    coord_down = (current_node.empty_tile_coordinate[0], current_node.empty_tile_coordinate[1] + 1)
    coord_right = (current_node.empty_tile_coordinate[0] + 1, current_node.empty_tile_coordinate[1])

    new_state = current_game_state.copy()

    if check_if_coord_inside_board(coord_up):
        # calculate the new state
        block_number = get_block_number_by_coordinates(coord_up)
        new_state = swap_numbers_in_list(0, block_number, new_state)
        # add the new child node to the open list
        new_child = Node(current_node, new_state, coord_up, current_node.g + 1, check_misplaced_blocks(new_state))
        child_list.append(new_child)

    new_state = current_game_state.copy()

    if check_if_coord_inside_board(coord_left):
        # calculate the new state
        block_number = get_block_number_by_coordinates(coord_left)
        new_state = swap_numbers_in_list(0, block_number, new_state)
        # add the new child node to the open list
        new_child = Node(current_node, new_state, coord_left, current_node.g + 1, check_misplaced_blocks(new_state))
        child_list.append(new_child)

    new_state = current_game_state.copy()

    if check_if_coord_inside_board(coord_right):
        # calculate the new state
        block_number = get_block_number_by_coordinates(coord_right)
        new_state = swap_numbers_in_list(0, block_number, new_state)
        # add the new child node to the open list
        new_child = Node(current_node, new_state, coord_right, current_node.g + 1, check_misplaced_blocks(new_state))
        child_list.append(new_child)

    new_state = current_game_state.copy()

    if check_if_coord_inside_board(coord_down):
        # calculate the new state
        block_number = get_block_number_by_coordinates(coord_down)
        new_state = swap_numbers_in_list(0, block_number, new_state)
        # add the new child node to the open list
        new_child = Node(current_node, new_state, coord_down, current_node.g + 1, check_misplaced_blocks(new_state))
        child_list.append(new_child)

    return child_list


def add_node_to_open_list(new_node):
    # if the list is empty, add it
    if len(open_list) == 0:
        open_list.append(new_node)
    else:
        open_list.append(new_node)
        open_list.sort(key=operator.attrgetter('f'), reverse=True)


def update_empty_tile_coord(new_coord):
    empty_tile_coord[0] = new_coord[0]
    empty_tile_coord[1] = new_coord[1]
    # print(empty_block[0])
    # empty_block[0].button_ref.master.grid(row=new_coord[1], column=new_coord[0])


def get_block_number_by_coordinates(coordinates):
    for x in block_list:
        if x.coordinate == coordinates:
            return x.number


def generate_start_state():
    # create a randomized list from 0-9
    random_number_list = list(range(9))
    random.shuffle(random_number_list)

    # create a 3x3 board
    counter = 0
    for i in range(3):
        for j in range(3):
            # this frame is one single "block"
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=0
            )
            # don't draw the box for the "0" tile
            # padding between the buttons
            frame.grid(row=i, column=j, padx=1, pady=1)
            button = tk.Button(master=frame,
                               text=random_number_list[counter],
                               image=pixelVirtual,
                               width=buttonSize,
                               height=buttonSize,
                               compound="center",
                               font=fontStyle
                               )

            button_coord = (j, i)
            # buttonInfo = (frame, button_coord)
            buttonCoordList.append(button_coord)
            current_state_list.append(random_number_list[counter])
            # create our block
            new_block = Block(button, random_number_list[counter], button_coord)
            block_list.append(new_block)
            # turn the 0 Button invisible
            if random_number_list[counter] == 0:
                frame.grid_forget()
                update_empty_tile_coord(button_coord)

            # bind the event to the click of the button and pass args
            button.bind("<Button-1>", lambda event, arg=new_block: handle_click(event, arg))
            button.pack(padx=0, pady=0)

            # increase counter
            counter += 1

    if check_if_solvable():
        print("started algorithm")
        solve_using_a_star()
    window.mainloop()


generate_start_state()
