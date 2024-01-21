import tkinter as tk
from tkinter.constants import NORMAL, DISABLED


BG = "#AAC8A7"
FILL = "#99A98F"
BFILL = "#183D3D"
CROSS = "❌"
CIRCLE = "⭕"

window = tk.Tk()
window.title("Tic Tac Toe")
window.geometry("350x450")
window.config(bg=BG)


def reset():
    global set_0, set_1
    set_0.clear()
    set_1.clear()
    for button in button_dict.values():
        button.config(text="", state=NORMAL, disabledforeground=BFILL)
    game_label.config(text="Tic Tac Toe")


reset_button = tk.Button(
            window,
            text="Play Again",
            font=("Times New Roman", 16, "normal"),
            padx=20, borderwidth=0,
            command=reset)

set_0, set_1 = set(), set()
count = 0


def make_button(loc, tag, button):
    button_dict[tag] = tk.Button(
            master=window,
            text="",
            width=3, borderwidth=0,
            bg=FILL, font=("Times New Roman", 35, "bold"),
            fg=BFILL, state=NORMAL, disabledforeground=BFILL,
            command=lambda: press(button))
    canvas.create_window(loc[0], loc[1], window=button_dict[tag])


winning_cases = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8},
                 {0, 4, 8}, {2, 4, 6},
                 {0, 3, 6}, {1, 4, 7}, {2, 5, 8}]


def check_win(set_list):
    for set_id in range(len(set_list)):
        for win_set in winning_cases:
            if win_set.issubset(set_list[set_id]):
                for index in win_set:
                    button_dict[f"B{index}"].config(disabledforeground="#BB2525")
                if set_id == 0:
                    game_label.config(text="\"Player X Wins\"")
                else:
                    game_label.config(text="\"Player O Wins\"")
                return True


def press(index):
    global count, set_1, set_0
    if count % 2 == 0:
        button_dict[f"B{index}"].config(text=CROSS, state=DISABLED)
        set_0.add(index)
    else:
        set_1.add(index)
        button_dict[f"B{index}"].config(text=CIRCLE, state=DISABLED)
    count += 1
    if check_win([set_0, set_1]):
        for button in button_dict.values():
            button.config(state=DISABLED)
        reset_button.pack()
    elif set_0.union(set_1) == {0, 1, 2, 3, 4, 5, 6, 7, 8}:
        for button in button_dict.values():
            button.config(disabledforeground="#8B7E74")
        game_label.config(text="\"Draw\"")
        reset_button.pack()


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
