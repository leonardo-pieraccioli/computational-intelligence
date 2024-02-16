from game import Game, Move, Player
import os

# Added to understand the game and play against my AI

class HumanPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        os.system('cls')
        board = game.get_board()
        print('  1  2  3  4  5')
        for index, row in enumerate(board):
            print(index + 1, end=' ')
            for cell in row:
                if cell == -1:
                    print('⬜️', end=' ')
                elif cell == 0:
                    print('❌', end=' ')
                elif cell == 1:
                    print('⭕️', end=' ')
            print()
        col = row = -1
        print("Take a piece from the border: ")
        while col < 0 or col > 5: col = int(input("Col: "))
        while row < 0 or row > 5: row = int(input("Row: "))
        from_pos = (row-1, col-1)
        
        print("Move it to: ")
        move = int(input("1. Top\n2. Bottom\n3. Left\n4. Right\n"))
        if move == 1: return from_pos, Move.TOP
        if move == 2: return from_pos, Move.BOTTOM
        if move == 3: return from_pos, Move.LEFT
        if move == 4: return from_pos, Move.RIGHT
        assert False, "Invalid move"