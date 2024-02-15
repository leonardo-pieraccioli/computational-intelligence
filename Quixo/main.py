from game import Game
from random_player import RandomPlayer
from minmax_player import MinmaxPlayer
import time as t
import tqdm.auto as tqdm

start_time = t.time()
NUM_GAMES = 10
win = [0, 0]

g = Game()
winner = g.play(MinmaxPlayer(0), RandomPlayer())
print(f'time elapsed: {t.time() - start_time}')
# with tqdm.trange(NUM_GAMES) as pbar:
#     for _ in range(NUM_GAMES):
#         g = Game()
#         winner = g.play(MinmaxPlayer(0), RandomPlayer())
#         win[winner] += 1
#         pbar.update(1)

# win_rate = win[0] / NUM_GAMES
# print(win_rate)

# win = [0, 0]
# with tqdm.trange(NUM_GAMES) as pbar:
#     for _ in range(10):
#         g = Game()
#         winner = g.play(RandomPlayer(), MinmaxPlayer(1))
#         win[winner] += 1
#         pbar.update(1)

# win_rate = win[1] / NUM_GAMES
# print(win_rate)

