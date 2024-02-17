from game import Game
from random_player import RandomPlayer
from minmax_player import MinmaxPlayer
from human_player import HumanPlayer
import time as t
import tqdm

print('List of games:\n\t1. Minmax (1) vs Random\n\t2. Random vs Minmax (1)\n\t3. Minmax (2) vs Random\n\t4. Random vs Minmax (2)\n\t5. Minmax (2) vs Minmax (1)\n\t6. Minmax (1) vs Minmax (2)\n\t7. Minmax (1) vs Minmax (1)\n\t8. Minmax (2) vs Minmax (2)\n')
NUM_GAMES = int(input('How many games do you want to play? '))
win = [0, 0]

# g = Game()
# winner = g.play(MinmaxPlayer(0), HumanPlayer(), True)

print('Win counters take into account the second player (1)')

print('Minmax (1) vs Random')
win = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win += g.play(MinmaxPlayer(0, 1), RandomPlayer())
        pbar.update(1)
print(win, ' games won by Random against Minmax (1)')

print('Random vs Minmax (1)')
win = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win += g.play(RandomPlayer(), MinmaxPlayer(1, 1))
        pbar.update(1)
        
print(win, ' games won by Minmax (1) against Random')

print('Minmax (2) vs Random')
win = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win += g.play(MinmaxPlayer(0, 2), RandomPlayer())
        pbar.update(1)
        
print(win, ' games won by Random against Minmax (2)')

print('Random vs Minmax (2)')
win = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win += g.play(RandomPlayer(), MinmaxPlayer(1, 2))
        pbar.update(1)

print(win, ' games won by Minmax (2) against Random')

print('Minmax (2) vs Minmax (1)')
win = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win += g.play(MinmaxPlayer(0, 2), MinmaxPlayer(1, 1))
        pbar.update(1)

print(win, ' games won by Minmax (2) against Minmax (1)')

print('Minmax (1) vs Minmax (2)')
win = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win += g.play(MinmaxPlayer(0, 1), MinmaxPlayer(1, 2))
        pbar.update(1)

print(win, ' games won by Minmax (1) against Minmax (2)')

print('Minmax (1) vs Minmax (1)')
win = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win += g.play(MinmaxPlayer(0, 1), MinmaxPlayer(1, 1))
        pbar.update(1)

print(win, ' games won by Minmax (1) against Minmax (2)')

print('Minmax (2) vs Minmax (2)')
win = 0
with tqdm.tqdm(total=NUM_GAMES) as pbar:
    for _ in range(NUM_GAMES):
        g = Game()
        win += g.play(MinmaxPlayer(0, 2), MinmaxPlayer(1, 2))
        pbar.update(1)

print(win, ' games won by Minmax (1) against Minmax (2)')

