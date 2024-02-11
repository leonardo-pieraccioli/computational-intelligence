from collections import deque
from dataclasses import dataclass
import os
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt

from time import sleep
from itertools import count, permutations

from environment import Environment
from parameters import *

from datetime import datetime

board=Environment(win_reward=5,draw_reward=0, lose_reward=-3)

player0_wins=0
player1_wins=0
draws=0


was_random=[False,False]

def update_stats(board:Environment, print_game):
    global player0_wins, player1_wins, draws
    v=board.check_win()
    if v==PLAYER0:
        player0_wins+=1
        if print_game: print("Player 0 wins")
    elif v==PLAYER1:
        player1_wins+=1
        if print_game: print("Player 1 wins")
    elif v==DRAW:
        draws+=1
        if print_game: print("Draw")
    else:
        return False
    return True

def print_board():
    global TRAINING
    f=lambda x: ('x' if x==PLAYER0 else 'o') if x!=-1 else ' '
    f_vec=np.vectorize(f)
    TRAINING=False
    os.system('cls')
    print(f"Player 0: {player0_wins}, Player 1: {player1_wins}, Draws:{draws}")
    print(f_vec(board.taken))
    sleep(0.8)

def play(player0, player1, max_games:int):
    print_board()
    t = 0
    print_game = False
    while t < max_games:
        player0.step(board)
        if t>max_games-5:
            print_game = True
            print_board()
        if update_stats(board, print_game):
            if print_game: sleep(0.5)
            board.reset()
            print_game = False
            t+=1
            continue
        
        player1.step(board)
        if t>max_games-5:
            print_game = True
            print_board()
        if update_stats(board, print_game):
            if print_game: sleep(0.5)
            board.reset()
            print_game = False
            t+=1
            continue

    f = open(f'Lab10_TicTacToe_Minmax/results{datetime.now().month}{datetime.now().day}{datetime.now().hour}{datetime.now().minute}{datetime.now().second}.txt', "a")
    f.write(f"Player {type(player0)}: {player0_wins}, Player {type(player1)}: {player1_wins}, Draws:{draws}\n")