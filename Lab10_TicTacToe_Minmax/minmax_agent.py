

class Minmax():
    def __init__(self, player):
        self.player = player

    def move(self, board):
        return self.minmax(board, self.player)