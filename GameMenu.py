import tkinter as tk
from tkinter import messagebox
import subprocess

# Global variable for AI difficulty
AI_DIFFICULTY = 1  # Default to Easy

# Function to set AI difficulty
def set_difficulty(level):
    global AI_DIFFICULTY
    AI_DIFFICULTY = level
    difficulty_label.config(text=f"Difficulty: {'Easy' if level == 1 else 'Medium' if level == 3 else 'Hard'}")

# Function to open Board.py for PvP or PvAI
def open_board(game_mode):
    try:
        if game_mode == 1:  # PvAI mode
            subprocess.run(["python", "Board.py", str(game_mode), str(AI_DIFFICULTY)])
        else:  # PvP mode
            subprocess.run(["python", "Board.py", str(game_mode)])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Board.py: {e}")

# Initialize the main window
root = tk.Tk()
root.title("Game Menu")
root.geometry("600x400")  # Doubled the window size

# Label for the menu
label = tk.Label(root, text="Are you ready to play?", font=("Arial", 28))
label.pack(pady=20)

# Difficulty buttons
difficulty_label = tk.Label(root, text="Difficulty: Easy", font=("Arial", 16))
difficulty_label.pack()

easy_button = tk.Button(root, text="Easy", font=("Arial", 14), command=lambda: set_difficulty(1))
easy_button.pack(pady=5)

medium_button = tk.Button(root, text="Medium", font=("Arial", 14), command=lambda: set_difficulty(3))
medium_button.pack(pady=5)

hard_button = tk.Button(root, text="Hard", font=("Arial", 14), command=lambda: set_difficulty(5))
hard_button.pack(pady=5)

# Button for Player vs Player
pvp_button = tk.Button(root, text="PvP", font=("Arial", 16), width=10, height=2, command=lambda: open_board(0))
pvp_button.pack(pady=10)

# Button for Player vs AI
pvai_button = tk.Button(root, text="PvAI", font=("Arial", 16), width=10, height=2, command=lambda: open_board(1))
pvai_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
