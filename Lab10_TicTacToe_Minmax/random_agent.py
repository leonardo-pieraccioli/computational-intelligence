from environment import Environment
from random import choice 
from parameters import *

class Random():
    def __init__(self,player):
        self.player=player
    
    def step(self, board:Environment):
        available = [ index for index, value in enumerate(board.taken.flatten()) if value == -1 ]
        if available != []:
            board.play(self.player, choice(available))