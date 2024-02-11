import tictactoe as ttt
from environment import Environment
from random_agent import Random
from minmax_agent import Minmax

board=Environment()


#ttt.play(Random(0), Random(1), 5010)
#ttt.play(Random(0), Minmax(1), 100, 5)
ttt.play(Minmax(0), Random(1), 10, 5)
ttt.play(Minmax(0), Minmax(1), 5, 5)

