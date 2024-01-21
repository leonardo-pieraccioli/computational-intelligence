from collections import deque
from dataclasses import dataclass
import math
import os
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
import random
from copy import deepcopy
from time import sleep
from itertools import count, permutations

DISCOUNT=.75
PLAYER0=0
PLAYER1=1
DRAW=-1
DECAY=5000
NON_FINAL='nf'
TRAINING=True
BLEND_FACTOR=0.99

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
            if player==PLAYER0:
                self.player0+=[self.board[pos[0],pos[1]]]
            else:
                self.player1+=[self.board[pos[0],pos[1]]]
    
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


class Agent1():

    def mask_selections(lookup, mask:bool):
        if mask:
            return lookup
        else:
            return -math.inf
    
    mask_selection=np.vectorize(mask_selections)

    def __init__(self,player ,max_mem=10000, decay=DECAY):
        self.player=player
        self.moves_done=0
        self.memory=[]
        self.lookup=dict() #Lookup table for the quality state-value
        self.state_frequency=dict()
        self.eps=0
        self.was_random=False
        self.decay=decay
    # The VALUE function takes in a STATE and gives the discounted reward obtainable from that state following the policy (don't care about action taken)
    # The QUALITY function takes in a STATE and an ACTION and gives the discounted reward obtainable from that state-action following the policy

    def step(self, board:Environment):
        # if not board.is_new_game:
        #     reward, final=board.check_win_player(self.player)
        #     if TRAINING:
        #         self.memory.append((self.state, self.action, reward))

        #     if final:
        #         self.memorize()
        #         self.memory.clear()
        #         return True, self.was_random

        available_mask=[i==-1 for i in board.state.reshape([9])]
        if not np.any(available_mask):
            return True, None
        self.state=deepcopy(board.taken_sets)
        self.action, self.was_random = self.select_action(board, available_mask,0.0,0.9,self.decay)
        res=board.play(self.player, self.action)

        return False, self.was_random
        #print(available_mask)

    def update_values(self):
        reward, final=board.check_win_player(self.player)
        if TRAINING:
            self.memory.append((self.state, self.action, reward))

        if final:
            self.memorize()
            self.memory.clear()
            return True
        else:
            return False


    # Saves in a lookup table the cumulative reward MEAN over all the times 
    # a certain action has been called on that state     

    def memorize(self):  #GOT IT MEMORIZED???
        if not TRAINING:
            return
        cumulative_reward=0
        while len(self.memory)>0:
            taken_sets, action, reward=self.memory.pop()

            cumulative_reward=reward+DISCOUNT*cumulative_reward

            if taken_sets not in self.lookup.keys():
                self.lookup[taken_sets]=[0 for _ in range(9)]
                self.state_frequency[taken_sets]=[0 for _ in range(9)]
            
            # It kinda works, but not enough 
            #self.lookup[taken_sets][action] *= self.state_frequency[taken_sets][action]
            self.lookup[taken_sets][action] += cumulative_reward
            self.state_frequency[taken_sets][action] +=1
            #self.lookup[taken_sets][action] /= self.state_frequency[taken_sets][action]
            
            # self.lookup[taken_sets][action] *= (1-BLEND_FACTOR)
            # self.lookup[taken_sets][action] += cumulative_reward*BLEND_FACTOR

            assert self.lookup[taken_sets][action] is not math.nan, f"Not a Number error {self.state_frequency}"

    
    def calc_value(self, taken_sets, available_mask) -> int:
        if(taken_sets in self.lookup.keys()):
            values=self.mask_selection(self.lookup[taken_sets], available_mask)
            return np.argmax(values), False
        else:
            return random.sample(range(9), k=1, counts=map(lambda s:1 if s else 0, available_mask))[0], True


    def select_action(self, board:Environment, available_mask, eps_end, eps_start, eps_decay):

        if TRAINING:
            self.eps=eps_end+math.exp(-1*self.moves_done/eps_decay)*(eps_start-eps_end)
        else:
            self.eps=0
        self.moves_done+=1
        if(random.random()<self.eps):
            return random.sample(range(9), k=1, counts=map(lambda s:1 if s else 0, available_mask))[0], True
        else:
            return self.calc_value(board.taken_sets, available_mask)
    
    
        


    
board=Environment(win_reward=5,draw_reward=0, lose_reward=-3)
player=0

player0_wins=0
player1_wins=0
draws=0

player0=Agent1(PLAYER0,DECAY)
player1=Agent1(PLAYER1, DECAY/5)

p0_finished=False
p1_finished=False
print(board.taken)

def update_stats(board:Environment):
    global player0_wins, player1_wins, draws
    v=board.check_win()
    if v==PLAYER0:
        player0_wins+=1
    if v==PLAYER1:
        player1_wins+=1
    if v==DRAW:
        draws+=1

def print_board(board:Environment):
    global TRAINING
    f=lambda x: ('x' if x==PLAYER0 else 'o') if x!=-1 else ' '
    f_vec=np.vectorize(f)
    TRAINING=False
    os.system('cls')
    print(f"Player 0: {player0_wins}, Player 1: {player1_wins}, Draws:{draws}, EPS0: {player0.eps}, EPS1: {player1.eps}")
    print(f_vec(board.taken))
    print(f"Player {player} random {was_random[player]}")
    sleep(1)

was_random=[False,False]
for t in count():
#  free=board.free

    p0_finished, was_random[0]=player0.step(board)
    if t>4*DECAY:
        print_board(board)
    p1_finished, was_random[1]=player1.step(board)
    if t>4*DECAY:
        print_board(board)

    p0_finished=player0.update_values()
    p1_finished=player1.update_values()

    update_stats(board)
    if(p0_finished or p1_finished):
        board.reset()

print(board.state)
print("Player ",player, " won")


        


    
