class GameManager:
    def __init__(self, players):
        self.players = {i + 1: 0 for i in range(players)}
        self.current_turn = 1

    def update_points(self, player):
        self.players[player] += 1

    def next_turn(self):
        self.current_turn = (self.current_turn % len(self.players)) + 1

    def get_winner(self):
        max_points = max(self.players.values())
        winners = [p for p, pts in self.players.items() if pts == max_points]
        return winners, max_points
