from copy import copy
from environment import Environment
from itertools import permutations
import numpy as np
from parameters import *
from tqdm.auto import tqdm
from time import sleep

MAGIC=np.array([1,6,5,8,4,0,3,2,7])
class Minmax():
    def __init__(self, player):
        self.player = player
        self.board = []
        self.rewards = [0, 0]
        self.rewards[player] = 1
        self.rewards[1-player] = -1

    def step(self, board: Environment):
        self.board = [ -1 if x == -1 else x for x in board.taken.flatten()]
        best_eval = float("-inf")
        for index, cell in enumerate(self.board):
            if cell != -1: continue
            self.board[index] = self.player
            eval = self.minmax(1-self.player, copy(self.board))             
            if eval > best_eval:
                best_move = index
                best_eval = eval
            self.board[index] = -1
                
        board.play(self.player, best_move)
        #print(f"Player {self.player} plays {best_move} with an evaluation of {best_eval}")
        #sleep(2)
    
    def minmax(self, current_player: int, board: list):
        result = self.check_win(board)
        if result != None: return result
        
        other_player = 1 - current_player
        best = float("-inf") if current_player == self.player else float("inf")
        
        for index, cell in enumerate(board):
            if cell != -1: continue
            board[index] = current_player
            evaluation = self.minmax(other_player, copy(board))
            board[index] = -1
            
            if current_player == self.player:
                best = max(evaluation, best)
            else:
                best = min(evaluation, best)
            
        return best

    def check_win(self, board):
        """Check if the game is over and return the result. If the game is not over, return None."""
        winner = None
        for i in range(0, 9, 3):
            if board[i] == board[i+1] == board[i+2] and board[i] != -1:
                winner = board[i]
    
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] and board[i] != -1:
                winner = board[i]
            
        if board[0] == board[4] == board[8] and board[4] != -1:
            winner = board[4]
        
        if board[2] == board[4] == board[6] and board[4] != -1:
            winner = board[4]
        
        if winner != None:
            return self.rewards[winner]
        
        elif not any([cell == -1 for cell in board]):
            return 0
        return None