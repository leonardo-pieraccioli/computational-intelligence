from parameters import *
import numpy as np
from itertools import permutations
from copy import deepcopy


class Environment():
    
    def __init__(self, win_reward=1, lose_reward=-1, draw_reward=1):
        self.board=np.array([[1,6,5],[8,4,0],[3,2,7]])
        self.taken=np.full([3,3],-1, dtype='int')
        self.player0=[]
        self.player1=[]
        self.win_reward=win_reward
        self.lose_reward=lose_reward
        self.draw_reward=draw_reward

    def reset(self):
        self.board=np.array([[1,6,5],[8,4,0],[3,2,7]])
        self.taken=np.full([3,3],-1, dtype='int')
        self.player0=[]
        self.player1=[]

    def check_win(self):
        if np.any([np.sum(p)==12 for p in permutations(self.player0,3)]):
            return PLAYER0
        elif np.any([np.sum(p)==12 for p in permutations(self.player1,3)]):
            return PLAYER1
        elif not np.any(self.taken==-1):
            return DRAW
        else: 
            return None
        
    def check_win_player(self, player):
        r=self.check_win()
        if r==None: 
            return 0, False
        elif r==DRAW:
            return self.draw_reward, True
        elif r==player:
            return self.win_reward, True
        else:
            return self.lose_reward, True
        
        
    def play(self, player, pos:int):
        pos=[pos//3, pos%3]

        if self.taken[pos[0],pos[1]]!=-1:
            return -1
        else:
            self.taken[pos[0],pos[1]]=player
        if player == 0:
            self.player0.append(self.board[pos[0],pos[1]])
        else:
            self.player1.append(self.board[pos[0],pos[1]])
    
    @property
    def free(self):
        l=[]
        for row in range(3):
            for col in range(3):
                if self.taken[row,col]==-1:
                    l+=[[row,col]]
        return l
    
    @property
    def state(self):
        return deepcopy(self.taken)
    
    @property
    def is_new_game(self):
        return np.count_nonzero(self.taken==False)<=1
    @property
    def taken_sets(self):
        return frozenset([frozenset(self.player0), frozenset(self.player1)])
