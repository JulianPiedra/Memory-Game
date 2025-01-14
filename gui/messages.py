import tkinter as tk

def show_winner(players, max_points, root):
    from gui.menu import start_menu
    message = ""
    if len(players) == 1:
        message = f"The winner is Player {players[0]} with {max_points} points!" 
    else:
        message = f"It's a draw, all players have {max_points} points!"
    tk.messagebox.showinfo("Game Over", message)
    root.destroy()
    start_menu()

    
