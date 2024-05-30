import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

root = tk.Tk()
root.title("Sudoku")

board = np.zeros((9, 9), dtype=int)
solution = np.zeros((9, 9), dtype=int)
entries = [[None for _ in range(9)] for _ in range(9)]

# ایجاد جدول سودوکو
for i in range(9):
    for j in range(9):
        entry = tk.Entry(root, width=2, font=('Arial', 18), justify='center')
        entry.grid(row=i, column=j)
        entries[i][j] = entry

check_button = tk.Button(root, text="Check", command=lambda: check_solution())
check_button.grid(row=9, column=4, columnspan=2)

# حل جدول سودوکو
def solve_sudoku(board):
    def find_empty(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(board, num, pos):
        row, col = pos
       
        # بررسی ردیف
        if num in board[row]:
            return False

        # بررسی ستون
        if num in [board[i][col] for i in range(9)]:
            return False

        # بررسی جعبه 3x3
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

# تولید جدول سودوکو
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
