from game import Game, Move, Player
from copy import deepcopy
import numpy as np
from time import sleep, time
from scipy.signal import convolve2d
from mm_utils import *

PLAYER0 = '❌'
PLAYER1 = '⭕️'
class MinmaxPlayer(Player):
    def __init__(self, player_id, max_depth=2) -> None:
        super().__init__()
        self._player_id = player_id
        self._eval_states = dict()
        self._max_depth = max_depth

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        # start_time = time()
        board = game.get_board()
        # g = Game(board)
        best = float("-inf")
        best_move = None
        
        for piece, slides in MOVES.items():
            if board[piece] != -1 and board[piece] != self._player_id: continue
            
            for slide in slides:
                ok = game.move((piece[1], piece[0]), slide, self._player_id)
                # print(f"Try move: {piece} {slide}")
                # game.print()

                assert ok == True, f'Invalid move, cell: {piece} move: {slide} something is wrong with the MOVES array.'
                prev_board = deepcopy(board)
                evaluation = self.__minmax(self._max_depth, 1 - self._player_id, game, float("-inf"), float("inf"))
                game.undo(prev_board)
                # print(f"Cancel move: {piece} {slide}")
                # game.print()
                
                if evaluation > best:
                    best = evaluation
                    best_move = (piece, slide)

        # game.print()
        # print(f'this state is evaluated: {self.__evaluate(-1, game.get_board(), self._player_id)}')
        # print(f'Player: {PLAYER0 if self._player_id == 0 else PLAYER1}, Best move: {best_move}, with evaluation: {best}')
        assert best != float("-inf") and best != float('inf'), "No move evaluated, or wrong init of best."
        # print(f'time elapsed: {time() - start_time}')
        return (best_move[0][1], best_move[0][0]), best_move[1]
    
    def __minmax(self, depth: int, current_player_id: int, game: Game, alpha: int, beta: int) -> int:
        '''Minmax algorithm. Returns the score of the board for the minmax player. The higher the better.'''
        board = game.get_board()
        winner = self.__check_winner(board)
        if depth == 0 or winner != -1:            
            eval = self.__evaluate(winner, board, current_player_id)
            # print(f'Eval: {eval}')
            # game.print()
            return eval
        
        other_player = 1 - current_player_id
        best = float("-inf") if current_player_id == self._player_id else float("inf")
        
        for piece, slides in MOVES.items():
            if board[piece] != -1 and board[piece] != current_player_id: continue
            
            for slide in slides:
                # print(f"Depth: {depth}, Try move {piece} {slide}")
                ok = game.move((piece[1], piece[0]), slide, current_player_id)
                assert ok == True, f'Invalid move, cell: {piece} move: {slide}'
                # game.print()
                prev_board = deepcopy(board)
                
                evaluation = self.__minmax(depth - 1, other_player, game, alpha, beta)
                # print(f"Player {current_player_id}, Move: {piece} {slide}, Evaluation: {evaluation}")
                # game.print()
                # sleep(1)
                
                game.undo(prev_board)
                # print(f"Depth: {depth}, Cancel move: {piece} {slide}")
                # game.print()

                if current_player_id == self._player_id:
                    best = max(evaluation, best)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
                else:
                    best = min(evaluation, best)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
                    
        assert best != float("-inf") and best != float('inf'), "No move evaluated, or wrong init of best."
        
        return best

    def __evaluate(self, winner: int, board, current_player: int) -> int:
        '''Evaluate a state. Returns the score of the board for the minmax player. The higher the better.'''
        
        # if there is a winner
        if winner == self._player_id:
            return E_WIN
        if winner == 1 - self._player_id:
            return -E_LOOSE
        
        # if the same state has already been evaluated
        board_str = ''.join([str(cell if cell != -1 else ' ') for cell in board.flatten()])
        board_str_90 = self.__rot90_string(board_str)
        board_str_180 = self.__rot90_string(board_str_90)
        board_str_270 = self.__rot90_string(board_str_180)
        board_str_inverted = self.__invert_players(board_str)
        
        for bstr in [board_str, board_str_90, board_str_180, board_str_270, board_str_inverted]:
            if bstr in self._eval_states: # add symmetries
                return self._eval_states[bstr]
        
        # evaluation 1: count the number of pieces of the player
        player_pieces = (board == self._player_id).sum()
        
        # evalutation 2: count the number of pieces in a row/column/diagonal for the player
        count4 = self.__count_consecutive(board, self._player_id, 4)
        count3 = self.__count_consecutive(board, self._player_id, 3) - count4
        count2 = self.__count_consecutive(board, self._player_id, 2) - count3 - count4*2
        
        # evaluation 3: count the number of pieces in a row/column/diagonal for the opponent
        count4_opponent = self.__count_consecutive(board, 1 - self._player_id, 4)
        count3_opponent = self.__count_consecutive(board, 1 - self._player_id, 3) - count4_opponent
        count2_opponent = self.__count_consecutive(board, 1 - self._player_id, 2) - count3_opponent - count4_opponent*2
        
        # total evaluation
        pos_evaluation = count4 * E_PLAYER_COUNT_4 + count3 * E_PLAYER_COUNT_3  + count2 * E_PLAYER_COUNT_2 + player_pieces * E_PLAYER_PIECES
        neg_evaluation = - count4_opponent * E_OPPONENT_COUNT_4 - count3_opponent * E_OPPONENT_COUNT_3 - count2_opponent * E_OPPONENT_COUNT_2
        evaluation = pos_evaluation + neg_evaluation
        
        self._eval_states[board_str] = evaluation
        
        if self._player_id == current_player:
            return evaluation
        return -evaluation
    
    def __count_consecutive(self, matrix, value, length):
        '''Count the number of consecutive values in a row, column or diagonal of a matrix'''
        
        # Create a filter for convolution
        filter_horizontal = np.ones((1, length))
        filter_vertical = np.ones((length, 1))
        filter_diagonal1 = np.eye(length)
        filter_diagonal2 = np.fliplr(filter_diagonal1)
        
        # Create a binary matrix for the given value
        binary_matrix = (matrix == value).astype(int)

        # Convolve the binary matrix with the filters
        horizontal = convolve2d(binary_matrix, filter_horizontal, mode='valid')
        vertical = convolve2d(binary_matrix, filter_vertical, mode='valid')
        diagonal1 = convolve2d(binary_matrix * np.eye(binary_matrix.shape[0], dtype=int), filter_diagonal1, mode='valid')
        diagonal2 = convolve2d(binary_matrix * np.fliplr(np.eye(binary_matrix.shape[0], dtype=int)), filter_diagonal2, mode='valid')

        # # Count the number of times the length appears in the convolutions
        count = 0
        for conv in [horizontal, vertical, diagonal1, diagonal2]:
            count += np.count_nonzero(conv == length)
    
        return count
    
    def __rot90_string(self, mat_str: str) -> str:
        '''Rotates the matrix string by 90 degrees'''
        mat_rot = [mat_str[i+5*j] for i in range(5) for j in range(5)]
        return ''.join(mat_rot)
    
    def __invert_players(self, board: str) -> str:
        '''Inverts the players in the matrix string'''
        return ''.join([str(1 - int(cell)) for cell in board if cell != ' '])
    
    def __check_winner(self, board) -> int:
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
