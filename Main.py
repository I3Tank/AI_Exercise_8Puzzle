# Needed for the GUI
import tkinter as tk
import tkinter.font as myFont
import random

from AStar import AStar
from Helper import Helper
import Board as Board
from Block import Block
from Player import Player

window = tk.Tk()
window.title("8-Puzzle")
# Center window on startup
window.eval('tk::PlaceWindow . center')
# create Menu bar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar)


buttonSize = 100
fontStyle = myFont.Font(size=20)

# create a 1x1 pixel to scale the buttons as squares
pixelVirtual = tk.PhotoImage(width=1, height=1)

frame_list = []


def create_solvable_board():
    # reset the board to generate a new one
    for frame in frame_list:
        frame.destroy()

    Board.current_state.clear()
    # create a randomized list from 0-9
    new_game_state = list(range(9))
    random.shuffle(new_game_state)

    # shuffle the list until we have a solvable state
    while not Helper.check_if_solvable(new_game_state):
        random.shuffle(new_game_state)

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
                               text=new_game_state[counter],
                               image=pixelVirtual,
                               width=buttonSize,
                               height=buttonSize,
                               compound="center",
                               font=fontStyle
                               )
            frame_list.append(frame)
            button_coord = (j, i)
            # buttonInfo = (frame, button_coord)
            Board.current_state.append(new_game_state[counter])
            # create our block
            new_block = Block(button, new_game_state[counter], button_coord)
            # turn the 0 Button invisible
            if new_game_state[counter] == 0:
                frame.grid_forget()
                Board.update_empty_coord((j, i))

            # bind the event to the click of the button and pass args
            button.bind("<Button-1>", lambda event, arg=new_block: Player.on_button_click(event, arg))
            button.pack(padx=0, pady=0)

            # increase counter
            counter += 1
    print(Board.current_state)

    window.mainloop()


filemenu.add_command(label="Reset Board", command=create_solvable_board)
filemenu.add_command(label="Start A*", command=AStar.solve_using_a_star)

menubar.add_cascade(label="Menu", menu=filemenu)
window.config(menu=menubar)

create_solvable_board()
