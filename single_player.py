import tkinter as tk
from tkinter.constants import NORMAL, DISABLED
import random

BG = "#BEADFA"
FILL = "#A8A196"
BFILL = "#5C4B99"
DRAW_FILL = "#DFCCFB"
GAME_OVER_FILL = "#BB2525"
RESET = "#5C4B99"
RESET_TEXT = "#FFFFFF"

CROSS = "❌"
CIRCLE = "⭕"
MASTER_SET = {0, 1, 2, 3, 4, 5, 6, 7, 8}
game_over = False

winning_cases = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8},
                 {0, 4, 8}, {2, 4, 6},
                 {0, 3, 6}, {1, 4, 7}, {2, 5, 8}]

set_0, set_1 = set(), set()

window = tk.Tk()
window.title("Tic Tac Toe")
window.geometry("350x450")
window.config(bg=BG)


def reset():
    global set_0, set_1, game_over
    game_over = False
    set_0.clear()
    set_1.clear()
    for button in button_dict.values():
        button.config(text="", state=NORMAL, disabledforeground=BFILL)
    game_label.config(text="Tic Tac Toe")


reset_button = tk.Button(
            window,
            text="Play Again",
            font=("Times New Roman", 16, "normal"),
            padx=20, borderwidth=0, bg=RESET, fg=RESET_TEXT,
            command=reset)


def make_button(loc, tag, button):
    button_dict[tag] = tk.Button(
            master=window,
            text="",
            width=3, borderwidth=0,
            bg=FILL, font=("Times New Roman", 35, "bold"),
            fg=BFILL, state=NORMAL, disabledforeground=BFILL,
            command=lambda: press(button))
    canvas.create_window(loc[0], loc[1], window=button_dict[tag])


def check_win(set_list):
    global game_over
    for set_id in range(len(set_list)):
        for win_set in winning_cases:
            if win_set.issubset(set_list[set_id]):
                for index in win_set:
                    button_dict[f"B{index}"].config(disabledforeground=GAME_OVER_FILL)
                if set_id == 0:
                    game_label.config(text="\"Player Wins\"")
                    game_over = True
                else:
                    game_label.config(text="\"Computer Wins\"")
                return True


def check_game_end():
    global set_0, set_1, game_over
    if check_win([set_0, set_1]):
        for button in button_dict.values():
            button.config(state=DISABLED)
        reset_button.pack()

    elif set_0.union(set_1) == MASTER_SET:
        game_over = True
        for button in button_dict.values():
            button.config(disabledforeground=DRAW_FILL)
        game_label.config(text="\"Draw\"")
        reset_button.pack()


def comp_win_cases(set_id):
    global set_0, set_1
    set_type = set()
    for win_set in winning_cases:
        if len(set_id) < 3:
            if set_id.issubset(win_set):
                set_type = (set_type.union(win_set.difference(set_id))).difference(set_0.union(set_1))
        else:
            times = len(set_id)
            for n in range(times):
                for elem in range(len(set_id)):
                    temp_set = set()
                    if elem < times - 1:
                        temp_set.add(list(set_id)[elem])
                        temp_set.add(list(set_id)[elem + 1])
                        if temp_set.issubset(win_set):
                            set_type = (set_type.union(win_set.difference(temp_set))).difference(set_0.union(set_1))
                    elif elem == times - 1:
                        elem -= times
                        temp_set.add(list(set_id)[elem])
                        temp_set.add(list(set_id)[elem + 1])
                        if temp_set.issubset(win_set):
                            set_type = (set_type.union(win_set.difference(temp_set))).difference(set_0.union(set_1))
    return set_type


def press(index):
    global set_1, set_0, game_over
    button_dict[f"B{index}"].config(text=CROSS, state=DISABLED)
    set_0.add(index)

    check_game_end()

    l_set = comp_win_cases(set_0)
    w_set = comp_win_cases(set_1)

    comp_input_list = list(l_set)*10+list(w_set)*1
    if len(comp_input_list) == 0:
        comp_input_list = list(MASTER_SET.difference(set_0.union(set_1)))

    if not game_over and len(comp_input_list) > 0:
        comp_index = random.choice(comp_input_list)
        set_1.add(comp_index)
        window.after(75, button_dict[f"B{comp_index}"].config(text=CIRCLE, state=DISABLED))

    check_game_end()


game_label = tk.Label(
    master=window,
    text="Tic Tac Toe",
    font=("Times New Roman", 26, "bold"),
    pady=30,
    bg=BG,
    fg="#183D3D")
game_label.pack()

canvas = tk.Canvas(master=window, width=300, height=300, bg=FILL)
canvas.pack()
canvas.create_line(100, 0, 100, 300, width=3, fill="white")
canvas.create_line(200, 0, 200, 300, width=3, fill="white")
canvas.create_line(0, 100, 300, 100, width=3, fill="white")
canvas.create_line(0, 200, 300, 200, width=3, fill="white")

button_dict = {}
locations = [
    (50, 50), (150, 50), (250, 50),
    (50, 150), (150, 150), (250, 150),
    (50, 250), (150, 250), (250, 250)
    ]


for i in range(len(locations)):
    make_button(locations[i], f"B{i}", i)

window.mainloop()
