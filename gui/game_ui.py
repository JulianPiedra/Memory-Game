import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from game.board import Board
from game.game_manager import GameManager
from game.card import Card
from gui.messages import show_winner

def start_game_ui(players, theme, mode):
    rows, cols = (4, 5) if mode == "Pairs" else (6, 5)
    card_paths = [f"assets/{theme.lower()}{i}.png" for i in range(1, 11)]
    cards = card_paths * (2 if mode == "Pairs" else 3)
    random.shuffle(cards)

    board = Board(rows, cols, cards)
    manager = GameManager(players)
    flipped_cards = []  # Keeps track of flipped cards
    matched_cards = set()  # Keeps track of matched card positions
    buttons = []  # Button references for GUI updates

    def handle_click(row, col):
        # Check if the card is already matched or flipped
        if (row, col) in matched_cards or (row, col) in flipped_cards:
            return

        # Check if two cards are already flipped, and prevent flipping more
        if len(flipped_cards) >= 2:
            return

        # Flip the card and update the board
        card_image = board.get_card(row, col).load_image()
        buttons[row][col].config(image=card_image)
        flipped_cards.append((row, col))

        # Check for matches
        if len(flipped_cards) == (2 if mode == "Pairs" else 3):
            root.after(1000, check_match)


    def check_match():
        nonlocal flipped_cards

        # Extract card paths to check if they match
        card_images = [board.get_card(row, col).image_path for row, col in flipped_cards]
        if len(set(card_images)) == 1:  # All flipped cards match
            for row, col in flipped_cards:
                matched_cards.add((row, col))
                buttons[row][col].config(state=tk.DISABLED)  # Disable matched buttons
            manager.update_points(manager.current_turn)
        else:  # Cards do not match, flip them back
            for row, col in flipped_cards:
                buttons[row][col].config(image=back_image)

        # Clear flipped cards and proceed to the next turn
        flipped_cards = []
        if len(matched_cards) == len(cards):  # Check if all cards are matched
            end_game()
        else:
            manager.next_turn()
            update_status()

    def update_status():
        status_label.config(text=f"Player {manager.current_turn}'s Turn - Points: {manager.players[manager.current_turn]}")

    def end_game():
        winners, max_points = manager.get_winner()
        show_winner(winners, max_points, root)

    # Create the main window
    root = tk.Tk()
    root.title("Memory Game")
    root.geometry(f"{cols * 120}x{rows * 120 + 50}")

    # Load the back image for cards
    global back_image
    back_image = Image.open("assets/carta_cerrada.png")
    back_image.thumbnail((100, 100))
    back_image = ImageTk.PhotoImage(back_image)

    # Create the game board UI
    for r in range(rows):
        button_row = []
        for c in range(cols):
            # Initialize cards in the board
            card = Card(cards[r * cols + c])
            board.place_card(r, c, card)

            # Create a button for each card
            btn = tk.Button(root, image=back_image, command=lambda r=r, c=c: handle_click(r, c))
            btn.grid(row=r, column=c, padx=5, pady=5)
            button_row.append(btn)
        buttons.append(button_row)

    # Status label for showing the current player's turn and points
    status_label = tk.Label(root, text=f"Player {manager.current_turn}'s Turn - Points: 0")
    status_label.grid(row=rows, column=0, columnspan=cols, pady=10)

    root.mainloop()
