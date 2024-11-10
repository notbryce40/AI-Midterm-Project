import tkinter as tk
from tkinter import messagebox
import subprocess

# Function to open Board.py for PvP or PvAI
def open_board(mode):
    ai_difficulty = difficulty_slider.get()  # Get the slider's current value
    try:
        # Pass difficulty as an argument only for PvAI mode
        if mode == "PvAI":
            subprocess.run(["python", "Board.py", mode, str(ai_difficulty)])
        else:
            subprocess.run(["python", "Board.py", mode])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Board.py: {e}")

# Initialize the main window
root = tk.Tk()
root.title("Game Menu")
root.geometry("600x400")  # Doubled the window size

# Label for the menu
label = tk.Label(root, text="Are you ready to play?", font=("Arial", 28))
label.pack(pady=20)  # Increased padding

# Difficulty slider
difficulty_label = tk.Label(root, text="Select Difficulty:", font=("Arial", 16))
difficulty_label.pack()
difficulty_slider = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL, length=400)  # Increased length
difficulty_slider.pack(pady=10)

# Button for Player vs Player
pvp_button = tk.Button(root, text="PvP", font=("Arial", 16), width=10, height=2, command=lambda: open_board("PvP"))
pvp_button.pack(pady=10)

# Button for Player vs AI
pvai_button = tk.Button(root, text="PvAI", font=("Arial", 16), width=10, height=2, command=lambda: open_board("PvAI"))
pvai_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
