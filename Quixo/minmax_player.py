from game import Game, Move, Player
import random
from copy import deepcopy
import numpy as np
from tqdm.auto import tqdm
from time import sleep

# evalutations 
E_WIN = 30
E_LOOSE = -30

# all possible moves
MOVES = {
    #corner moves
    (0, 0): [Move.BOTTOM, Move.RIGHT],
    (0, 4): [Move.BOTTOM, Move.LEFT],
    (4, 0): [Move.TOP, Move.RIGHT],
    (4, 4): [Move.TOP, Move.LEFT],
    
    # high border moves
    (0, 1): [Move.BOTTOM, Move.RIGHT, Move.LEFT],
    (0, 2): [Move.BOTTOM, Move.RIGHT, Move.LEFT],
    (0, 3): [Move.BOTTOM, Move.RIGHT, Move.LEFT],
    
    # low border moves
    (4, 1): [Move.TOP, Move.RIGHT, Move.LEFT],
    (4, 2): [Move.TOP, Move.RIGHT, Move.LEFT],
    (4, 3): [Move.TOP, Move.RIGHT, Move.LEFT],
    
    # left border moves
    (1, 0): [Move.BOTTOM, Move.TOP, Move.RIGHT],
    (2, 0): [Move.BOTTOM, Move.TOP, Move.RIGHT],
    (3, 0): [Move.BOTTOM, Move.TOP, Move.RIGHT],
    
    # right border moves
    (1, 4): [Move.BOTTOM, Move.TOP, Move.LEFT],
    (2, 4): [Move.BOTTOM, Move.TOP, Move.LEFT],
    (3, 4): [Move.BOTTOM, Move.TOP, Move.LEFT],
}

OLD_ARRAY_MOVES = [
    # corner moves
    ((0, 0), Move.BOTTOM), 
    ((0, 0), Move.RIGHT),
    ((0, 4), Move.BOTTOM),
    ((0, 4), Move.LEFT),
    ((4, 0), Move.TOP),
    ((4, 0), Move.RIGHT),
    ((4, 4), Move.TOP),
    ((4, 4), Move.LEFT),
    
    # high border moves
    ((0, 1), Move.BOTTOM),
    ((0, 2), Move.BOTTOM),
    ((0, 3), Move.BOTTOM),
    ((0, 1), Move.RIGHT),
    ((0, 2), Move.RIGHT),
    ((0, 3), Move.RIGHT),
    ((0, 1), Move.LEFT),
    ((0, 2), Move.LEFT),
    ((0, 3), Move.LEFT),
    
    # low border moves
    ((4, 1), Move.TOP),
    ((4, 2), Move.TOP),
    ((4, 3), Move.TOP),
    ((4, 1), Move.LEFT),
    ((4, 2), Move.LEFT),
    ((4, 3), Move.LEFT),
    ((4, 1), Move.RIGHT),
    ((4, 2), Move.RIGHT),
    ((4, 3), Move.RIGHT),
    
    # left border moves
    ((1, 0), Move.RIGHT),
    ((2, 0), Move.RIGHT),
    ((3, 0), Move.RIGHT),
    ((1, 0), Move.BOTTOM),
    ((2, 0), Move.BOTTOM),
    ((3, 0), Move.BOTTOM),
    ((1, 0), Move.TOP),
    ((2, 0), Move.TOP),
    ((3, 0), Move.TOP),
    
    # right border moves
    ((1, 4), Move.LEFT),
    ((2, 4), Move.LEFT),
    ((3, 4), Move.LEFT),
    ((1, 4), Move.TOP),
    ((2, 4), Move.TOP),
    ((3, 4), Move.TOP),
    ((1, 4), Move.BOTTOM),
    ((2, 4), Move.BOTTOM),
    ((3, 4), Move.BOTTOM),
    ]
class MinmaxPlayer(Player):
    def __init__(self, player_id, max_depth=2) -> None:
        super().__init__()
        self._player_id = player_id
        self._eval_states = dict()
        self._max_depth = max_depth

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        board = game.get_board()
        # g = Game(board)
        best = float("-inf")
        best_move = None
        
        # with tqdm(total=len(MOVES)) as pbar:
        for piece, slides in MOVES.items():
            if board[piece] != -1 and board[piece] != self._player_id: continue
            
            for slide in slides:
                ok = game.move(piece, slide, self._player_id)
                # print("Depth: 0, Tento mossa")
                # game.print()

                assert ok == True, f'Invalid move, cell: {piece} move: {slide} something is wrong with the MOVES array.'
                prev_board = deepcopy(board)
                evaluation = self._minmax(self._max_depth, 1 - self._player_id, game)
                game.undo(prev_board)
                # print("Depth: 0, Mossa annullata")
                # game.print()
                
                if evaluation > best:
                    best = evaluation
                    best_move = (piece, slide)
            # pbar.update(1)
        assert best != float("-inf") and best != float('inf'), "No move evaluated, or wrong init of best."
        # print(best_move)
        return best_move[0], best_move[1]
    
    def _minmax(self, depth: int, current_player_id: int, game: Game) -> int:
        board = game.get_board()
        winner = self._check_winner(board)
        if depth == 0 or winner != -1:
            return self._evaluate(winner, board)
        
        other_player = 1 - current_player_id
        best = float("-inf") if current_player_id == self._player_id else float("inf")
        
        for piece, slides in MOVES.items():
            if board[piece] != -1 and board[piece] != current_player_id: continue
            
            for slide in slides:
                # print(f"Depth: {depth}, Tento mossa: {piece} {slide}")
                ok = game.move(piece, slide, current_player_id)
                # game.print()
                
                assert ok == True, f'Invalid move, cell: {piece} move: {slide}'
                prev_board = deepcopy(board)
                evaluation = self._minmax(depth - 1, other_player, game)
                
                game.undo(prev_board)
                # print(f"Depth: {depth}, Mossa annullata: {piece} {slide}")
                # game.print()
            
            if current_player_id == self._player_id:
                best = max(evaluation, best)
            else:
                best = min(evaluation, best)

        assert best != float("-inf") and best != float('inf'), "No move evaluated, or wrong init of best."
        return best

    def _evaluate(self, winner: int, board) -> int:
        # if there is a winner
        if winner == self._player_id:
            return E_WIN
        if winner == 1 - self._player_id:
            return -E_LOOSE
        
        # if the same state has already been evaluated
        board_str = ''.join([str(cell) for cell in board.flatten()])
        if board_str in self._eval_states: # add symmetries
            return self._eval_states[board_str]
        
        # evaluation 1: count the number of pieces of the player
        player_pieces = (board == self._player_id).sum()
        
        # evalutation 2: count the number of pieces in a row/column/diagonal for the player
        
        return player_pieces

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
