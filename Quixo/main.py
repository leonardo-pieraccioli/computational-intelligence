from game import Game
from random_player import RandomPlayer
from minmax_player import MinmaxPlayer
from human_player import HumanPlayer
import time as t
import tqdm

NUM_GAMES = 20
win = [0, 0]

# g = Game()
# winner = g.play(MinmaxPlayer(0), HumanPlayer(), True)

win1 = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win1 += g.play(MinmaxPlayer(0, 1), RandomPlayer())
        pbar.update(1)


print(win1)

win2 = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win2 += g.play(MinmaxPlayer(1, 2), MinmaxPlayer(1, 1))
        pbar.update(1)

print(win2)

win3 = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win3 += g.play(MinmaxPlayer(1, 1), MinmaxPlayer(1, 2))
        pbar.update(1)

print(win3)