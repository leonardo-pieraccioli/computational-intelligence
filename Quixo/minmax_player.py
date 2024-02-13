from game import Game, Move, Player
import random
from copy import copy

class MinmaxPlayer(Player):
    def __init__(self, player_id, board) -> None:
        super().__init__()
        self._player_id = player_id

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        pass
    
    def _minmax(self, depth: int, current_player_id: int, board) -> int:
        if depth == 0 or self._check_winner() != -1:
            return self._evaluate(board)
        
        other_player = 1 - current_player_id
        best = float("-inf") if current_player_id == self._player_id else float("inf")
        
        for index, cell in enumerate(board):
            if cell != -1: continue
            board[index] = current_player_id
            evaluation = self._minmax(depth - 1, other_player, copy(board))
            board[index] = -1
            
            if current_player_id == self._player_id:
                best = max(evaluation, best)
            else:
                best = min(evaluation, best)
            
        return best

    def _evaluate(self, board) -> int:
        pass

    def _check_winner(self, board) -> int:
        '''Check the winner. Returns the player ID of the winner if any, otherwise returns -1'''
        # for each row
        for x in range(board.shape[0]):
            # if a player has completed an entire row
            if board[x, 0] != -1 and all(board[x, :] == board[x, 0]):
                # return the relative id
                return board[x, 0]
        # for each column
        for y in range(board.shape[1]):
            # if a player has completed an entire column
            if board[0, y] != -1 and all(board[:, y] == board[0, y]):
                # return the relative id
                return board[0, y]
        # if a player has completed the principal diagonal
        if board[0, 0] != -1 and all(
            [board[x, x]
                for x in range(board.shape[0])] == board[0, 0]
        ):
            # return the relative id
            return board[0, 0]
        # if a player has completed the secondary diagonal
        if board[0, -1] != -1 and all(
            [board[x, -(x + 1)]
             for x in range(board.shape[0])] == board[0, -1]
        ):
            # return the relative id
            return board[0, -1]
        return -1