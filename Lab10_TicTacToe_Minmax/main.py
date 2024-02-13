import tictactoe as ttt
from environment import Environment
from random_agent import Random
from minmax_agent import Minmax

board=Environment()


#ttt.play(Random(0), Random(1), 10,1)
ttt.play(Minmax(0), Random(1), 100, 1)
ttt.play(Random(0), Minmax(1), 100, 1)
ttt.play(Minmax(0), Minmax(1), 100, 1)
