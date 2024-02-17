# Quixo Project by Leonardo Pieraccioli (s318935)

For the project I sumbitted a Minmax solution with alpha beta pruning. 

## How to run the game

To run the game you need to launch the main.py file. By changing the players in the main file you can play against the AI or watch the AI play against itself. The game is played in the terminal.

The whole project was developed in Python 3.11.5 and tested on Windows 11 using the Poetry package manager. The project should work on any OS and Python 3.8+ but this has not been tested.

## Changes to the given code

game.py:
1. ```print```: now the board is printed in a pleasant way, with emojis and colors.
2. ```play```: added ```watch``` argument to print the board at each move. This has been useful to watch the game while the AI is playing.
3. ```move```: is now a public function to be able to try moves from the minmax algorithm.
4. ```undo```: is a new function to change the board. Is used by minmax to revert the board to a previous state.

added files:
1. ```main.py```: the main file to run the game. It contains the calls to the game loop and a few matches with different players.
2. ```human_player.py```: a player that asks the user for the move. Used to understand the game and analyze strategies (also to let my friends play against my AI)
3. ```minmax_player.py```: the minmax player. Contains the recursive algorithm, the evaluation function and the check for terminal states.
4. ```mm_utils.py```: data structures and utility functions used by the minmax algorithm.
5. ```random_player.py```: a player that makes random moves. Used to test against the minmax player. I just moved the given code in a separate file for clarity.
6. ```utility_test.ipynb```: a jupyter notebook to unit test the utility functions, the evaluation function and all the parts of the code I needed in other files.

