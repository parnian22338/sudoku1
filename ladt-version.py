
import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
import time

def start_game():
    global player_name, start_time, timer_running
    player_name = name_entry.get()
    if not player_name:
        messagebox.showerror("Error", "Please enter your name before starting.")
        return
    start_time = time.time()
    timer_running = True
    update_timer()
    start_button.config(state='disabled')
    name_entry.config(state='disabled')

def update_timer():
    if timer_running:
        elapsed_time = int(time.time() - start_time)
        time_label.config(text=f"Time: {elapsed_time}s")
        root.after(1000, update_timer)

def solve_sudoku(board):
    def find_empty(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(board, num, pos):
        row, col = pos

        if num in board[row]:
            return False

        if num in [board[i][col] for i in range(9)]:
            return False

        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num:
                    return False

        return True

    empty = find_empty(board)
    if not empty:
        return board
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve_sudoku(board):
                return board
            board[row][col] = 0

    return None

def check_solution():
    global timer_running
    user_board = np.zeros((9, 9), dtype=int)
    for i in range(9):
        for j in range(9):
            value = entries[i][j].get()
            if value.isdigit():
                user_board[i][j] = int(value)
            else:
                messagebox.showerror("Error", "Please enter valid numbers in all cells.")
                return

    if np.array_equal(user_board, solution):
        timer_running = False
        elapsed_time = int(time.time() - start_time)
        leaderboard.append((player_name, elapsed_time))
        leaderboard.sort(key=lambda x: x[1])
        messagebox.showinfo("Success", f"Congratulations {player_name}! You solved the Sudoku in {elapsed_time} seconds!")
    else:
        messagebox.showerror("Error", "The solution is not correct. Try again.")

def show_solution():
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state='normal')
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(solution[i][j]))
            if board[i][j] != 0:
                entries[i][j].config(state='disabled')

def show_leaderboard():
    leaderboard_text = "Leaderboard:\n"
    for idx, (name, time) in enumerate(leaderboard[:10], 1):
        leaderboard_text += f"{idx}. {name}: {time}s\n"
    messagebox.showinfo("Leaderboard", leaderboard_text)

def switch_to_dark_mode():
    root.config(bg='#2e2e2e')
    time_label.config(bg='#2e2e2e', fg='white')
    name_label.config(bg='#2e2e2e', fg='white')
    start_button.config(bg='#444444', fg='white')
    check_button.config(bg='#444444', fg='white')
    show_solution_button.config(bg='#444444', fg='white')
    leaderboard_button.config(bg='#444444', fg='white')
    dark_mode_button.config(bg='#444444', fg='white')
    light_mode_button.config(bg='#444444', fg='white')
    for row in entries:
        for entry in row:
            entry.config(bg='#3e3e3e', fg='white', insertbackground='white')

def switch_to_light_mode():
    root.config(bg='white')
    time_label.config(bg='white', fg='black')
    name_label.config(bg='white', fg='black')
    start_button.config(bg='lightgray', fg='black')
    check_button.config(bg='lightgray', fg='black')
    show_solution_button.config(bg='lightgray', fg='black')
    leaderboard_button.config(bg='lightgray', fg='black')
    dark_mode_button.config(bg='lightgray', fg='black')
    light_mode_button.config(bg='lightgray', fg='black')
    for row in entries:
        for entry in row:
            entry.config(bg='white', fg='black', insertbackground='black')

root = tk.Tk()
root.title("Sudoku")

player_name = None
start_time = None
timer_running = False
time_label = tk.Label(root, text="Time: 0s", font=('Arial', 20))
time_label.grid(row=12, column=0, columnspan=9)

board = np.zeros((9, 9), dtype=int)
solution = np.zeros((9, 9), dtype=int)
entries = [[None for _ in range(9)] for _ in range(9)]

leaderboard = []

name_label = tk.Label(root, text="Name:", font=('Arial', 14))
name_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))
name_entry = tk.Entry(root, font=('Arial', 14))
name_entry.grid(row=0, column=2, columnspan=7, pady=(10, 5))

for i in range(9):
    for j in range(9):
        entry = tk.Entry(root, width=3, font=('Arial', 20), justify='center')
        entry.grid(row=i+1, column=j)
        entries[i][j] = entry

start_button = tk.Button(root, text="Start", command=start_game)
start_button.grid(row=10, column=0, columnspan=2)

check_button = tk.Button(root, text="Check", command=lambda: check_solution())
check_button.grid(row=10, column=2, columnspan=2)

show_solution_button = tk.Button(root, text="Show Solution", command=lambda: show_solution())
show_solution_button.grid(row=10, column=4, columnspan=2)

leaderboard_button = tk.Button(root, text="Leaderboard", command=lambda: show_leaderboard())
leaderboard_button.grid(row=10, column=6, columnspan=2)

dark_mode_button = tk.Button(root, text="Dark Mode", command=switch_to_dark_mode)
dark_mode_button.grid(row=11, column=0, columnspan=4)

light_mode_button = tk.Button(root, text="Light Mode", command=switch_to_light_mode)
light_mode_button.grid(row=11, column=4, columnspan=4)

solution = solve_sudoku(np.zeros((9, 9), dtype=int).tolist())
if solution is None:
    raise Exception("Failed to generate a valid Sudoku board")

board = np.array(solution)
for _ in range(40):
    i, j = random.randint(0, 8), random.randint(0, 8)
    board[i][j] = 0

for i in range(9):
    for j in range(9):
        entries[i][j].delete(0, tk.END)
        if board[i][j] != 0:
            entries[i][j].insert(0, str(board[i][j]))
            entries[i][j].config(state='disabled')
        else:
            entries[i][j].config(state='normal')

root.mainloop()