import tkinter as tk
from gui.game_ui import start_game_ui

def start_menu():
    def start_game():
        num_players = 0
        try:
            num_players = int(entry_players.get())  # Convert input to an integer
            if num_players <= 0:
                raise ValueError  # Raise an error for invalid player numbers
        except ValueError:
            errorLabel.config(text="Please enter a valid number of players.", fg="red")
            return
        theme = theme_var.get()
        mode = mode_var.get()
        root.destroy()
        start_game_ui(num_players, theme, mode)

    root = tk.Tk()
    root.title("Memory Game Menu")
    root.geometry("250x270")
    root.resizable(False, False)
    tk.Label(root, text="Select Theme:").pack()
    theme_var = tk.StringVar(value="fruta")
    tk.Radiobutton(root, text="Fruits", variable=theme_var, value="fruta").pack()
    tk.Radiobutton(root, text="Sports", variable=theme_var, value="deporte").pack()
    tk.Radiobutton(root, text="Video Games", variable=theme_var, value="videojuego").pack()

    tk.Label(root, text="Game Mode:").pack()
    mode_var = tk.StringVar(value="Pairs")
    tk.Radiobutton(root, text="Pairs", variable=mode_var, value="Pairs").pack()
    tk.Radiobutton(root, text="Triplets", variable=mode_var, value="Triplets").pack()
    
    tk.Label(root, text="Number of Players:").pack()
    errorLabel = tk.Label(root, text="")
    entry_players = tk.Entry(root)
    entry_players.pack()
    errorLabel.pack()

    tk.Button(root, text="Start Game", command=start_game).pack()
    root.mainloop()
