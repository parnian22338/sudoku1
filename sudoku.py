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

root.mainloop()