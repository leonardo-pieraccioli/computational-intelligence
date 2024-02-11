from copy import deepcopy
from environment import Environment
from itertools import permutations
import numpy as np
from parameters import *

MAGIC=np.array([1,6,5,8,4,0,3,2,7])
class Minmax():
    def __init__(self, player):
        self.player = player
        self.board = []

    def step(self, board: Environment):
        self.board = board.taken.flatten()
        not_taken = [index for index, value in enumerate(self.board) if value == -1]
        best_eval = float("-inf")
        
        n_moves = len(not_taken)
        for _ in range(n_moves):
            move = not_taken.pop(0)
            self.board[move] = self.player
            eval = self.minmax(self.player, deepcopy(not_taken))
            if eval > best_eval:
                best = move
                best_eval = eval
            self.board[move] = -1
            not_taken.append(move)
        board.play(self.player, best)
    
    
    def minmax(self, player, not_taken):
        winner = self.check_win()
        if (winner == 0 and self.player == 0) or (winner == 1 and self.player == 1):
            return 1
        elif (winner == 1 and self.player == 0) or (winner == 0 and self.player == 1):
            return -1
        elif winner == DRAW:
            return 0
        else:
            if player == self.player:
                best = -2
                while not_taken:
                    next = not_taken.pop(0)
                    self.board[next] = player
                    best = max(best, self.minmax(1-self.player, deepcopy(not_taken)))
                    self.board[next] = -1
                return best
            else:
                best = 2
                while not_taken:
                    next = not_taken.pop(0)
                    self.board[next] = player
                    best = min(best, self.minmax(self.player, deepcopy(not_taken)))
                    self.board[next] = -1
                return best
            
    def check_win(self):
        player0 = []
        player1 = []
        for index, n in enumerate(self.board):
            if n == self.player:
                player0.append(MAGIC[index])
            elif n == 1-self.player:
                player1.append(MAGIC[index])
        if np.any([np.sum(p)==12 for p in permutations(player0,3)]):
            return 0
        elif np.any([np.sum(p)==12 for p in permutations(player1,3)]):
            return 1
        elif len(player0) + len(player1) == 9:
            return -1
        else: 
            return None