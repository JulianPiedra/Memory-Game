class Board:
    def __init__(self, rows, cols, cards):
        self.rows = rows
        self.cols = cols
        self.cards = cards
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]

    def place_card(self, row, col, card):
        self.board[row][col] = card

    def is_empty(self, row, col):
        return self.board[row][col] == ' '

    def get_card(self, row, col):
        return self.board[row][col]
