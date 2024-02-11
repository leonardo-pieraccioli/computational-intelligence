import math
import random
from copy import deepcopy
import numpy as np

from environment import Environment
from parameters import *

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

    def update_values(self, board:Environment):
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
    