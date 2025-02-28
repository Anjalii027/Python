import tkinter as tk
import random

root = tk.Tk()
root.title("Snake and Ladder Game")

snakes_and_ladders = {
    2: 38, 7: 14, 8: 31, 21: 42, 28: 84, 36: 44, 46: 25, 49: 11, 51: 67,
    62: 19, 64: 60, 71: 91, 74: 53, 80: 100, 89: 26, 92: 51, 95: 37, 99: 80
}

player1_position = 0
player2_position = 0
turn = 0

def roll_dice():
    return random.randint(1, 6)

def move_player(player_num, roll):
    global player1_position, player2_position, turn
    if player_num == 1:
        player1_position += roll
        if player1_position in snakes_and_ladders:
            player1_position = snakes_and_ladders[player1_position]
        if player1_position > 100:
            player1_position = 100
        if player1_position == 100:
            result_label.config(text="Player 1 wins!")
            return
        turn = 1
    else:
        player2_position += roll
        if player2_position in snakes_and_ladders:
            player2_position = snakes_and_ladders[player2_position]
        if player2_position > 100:
            player2_position = 100
        if player2_position == 100:
            result_label.config(text="Player 2 wins!")
            return
        turn = 0

    update_positions()
    draw_board()

def update_positions():
    player1_label.config(text=f"Player 1: {player1_position}")
    player2_label.config(text=f"Player 2: {player2_position}")
    roll_button.config(state=tk.NORMAL)

def on_roll():
    roll = roll_dice()
    roll_label.config(text=f"Dice Rolled: {roll}")
    roll_button.config(state=tk.DISABLED)
    if turn == 0:
        move_player(1, roll)
    else:
        move_player(2, roll)

def draw_board():
    canvas.delete("all")
    square_size = 50
    for row in range(10):
        for col in range(10):
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            # New color scheme for board squares
            if (row + col) % 2 == 0:
                color = "#90EE90"  # Light Green
            else:
                color = "#ADD8E6"  # Light Blue
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            square_number = 100 - (row * 10 + col)
            canvas.create_text(x1 + square_size // 2, y1 + square_size // 2, text=str(square_number))

    for start, end in snakes_and_ladders.items():
        start_row = 9 - (start - 1) // 10
        start_col = (start - 1) % 10
        end_row = 9 - (end - 1) // 10
        end_col = (end - 1) % 10
        start_x = start_col * square_size + square_size // 2
        start_y = start_row * square_size + square_size // 2
        end_x = end_col * square_size + square_size // 2
        end_y = end_row * square_size + square_size // 2

        if end > start:  # Ladder
            canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, width=5, fill="green")
        else:  # Snake
            canvas.create_line(start_x, start_y, end_x, end_y, width=5, fill="red", dash=(4, 2))

    player1_row = 9 - (player1_position - 1) // 10
    player1_col = (player1_position - 1) % 10
    player2_row = 9 - (player2_position - 1) // 10
    player2_col = (player2_position - 1) % 10

    player1_x = player1_col * square_size + square_size // 2
    player1_y = player1_row * square_size + square_size // 2
    player2_x = player2_col * square_size + square_size // 2
    player2_y = player2_row * square_size + square_size // 2

    canvas.create_oval(player1_x - 15, player1_y - 15, player1_x + 15, player1_y + 15, fill="blue")
    canvas.create_oval(player2_x - 15, player2_y - 15, player2_x + 15, player2_y + 15, fill="green")

title_label = tk.Label(root, text="Snake and Ladder Game", font=("Arial", 24))
title_label.grid(row=0, column=0, columnspan=2)

canvas = tk.Canvas(root, width=500, height=500)
canvas.grid(row=1, column=0, rowspan=5)

player1_label = tk.Label(root, text=f"Player 1: {player1_position}", font=("Arial", 14))
player1_label.grid(row=1, column=1)

player2_label = tk.Label(root, text=f"Player 2: {player2_position}", font=("Arial", 14))
player2_label.grid(row=2, column=1)

roll_label = tk.Label(root, text="Dice Rolled: ", font=("Arial", 14))
roll_label.grid(row=3, column=1)

roll_button = tk.Button(root, text="Roll Dice", font=("Arial", 14), command=on_roll)
roll_button.grid(row=4, column=1)

result_label = tk.Label(root, text="", font=("Arial", 16))
result_label.grid(row=5, column=0, columnspan=2)

root.mainloop()
