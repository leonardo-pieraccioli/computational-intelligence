from game import Game
from random_player import RandomPlayer
from minmax_player import MinmaxPlayer
from human_player import HumanPlayer
import time as t

NUM_GAMES = 10
win = [0, 0]

# g = Game()
# winner = g.play(MinmaxPlayer(0), HumanPlayer(), True)

win1 = 0
for _ in range(NUM_GAMES):
    g = Game()
    win1 += g.play(MinmaxPlayer(0, 1), RandomPlayer())
    t.sleep(1)

win2 = 0
for _ in range(NUM_GAMES):
    g = Game()
    win2 += g.play(MinmaxPlayer(1, 2), MinmaxPlayer(1, 1))
    t.sleep(1)

print(win1, win2)