class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.points = 0

    def add_point(self):
        self.points += 1
