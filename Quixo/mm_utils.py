from game import Move

# evalutations 
E_WIN = 500     # needs to be calculated looking at the maximum possible score considering the other paratemers
E_LOOSE = -500

E_PLAYER_COUNT_4 = 100      # has be higher than the max possible number of count_3
E_PLAYER_COUNT_3 = 10        # has be higher than the max possible number of count_2
E_PLAYER_COUNT_2 = 1

E_OPPONENT_COUNT_4 = 100     # has be higher than the max possible number of count_3
E_OPPONENT_COUNT_3 = 10      # has be higher than the max possible number of count_2
E_OPPONENT_COUNT_2 = 1

E_PLAYER_PIECES = 0.1

# all possible moves
MOVES = {
    #corner moves
    (0, 0): [Move.BOTTOM, Move.RIGHT],
    (0, 4): [Move.BOTTOM, Move.LEFT],
    (4, 0): [Move.TOP, Move.RIGHT],
    (4, 4): [Move.TOP, Move.LEFT],
    
    # high border moves
    (0, 1): [Move.BOTTOM, Move.RIGHT, Move.LEFT],
    (0, 2): [Move.BOTTOM, Move.RIGHT, Move.LEFT],
    (0, 3): [Move.BOTTOM, Move.RIGHT, Move.LEFT],
    
    # low border moves
    (4, 1): [Move.TOP, Move.RIGHT, Move.LEFT],
    (4, 2): [Move.TOP, Move.RIGHT, Move.LEFT],
    (4, 3): [Move.TOP, Move.RIGHT, Move.LEFT],
    
    # left border moves
    (1, 0): [Move.BOTTOM, Move.TOP, Move.RIGHT],
    (2, 0): [Move.BOTTOM, Move.TOP, Move.RIGHT],
    (3, 0): [Move.BOTTOM, Move.TOP, Move.RIGHT],
    
    # right border moves
    (1, 4): [Move.BOTTOM, Move.TOP, Move.LEFT],
    (2, 4): [Move.BOTTOM, Move.TOP, Move.LEFT],
    (3, 4): [Move.BOTTOM, Move.TOP, Move.LEFT],
}


# OLD_ARRAY_MOVES = [
#     # corner moves
#     ((0, 0), Move.BOTTOM), 
#     ((0, 0), Move.RIGHT),
#     ((0, 4), Move.BOTTOM),
#     ((0, 4), Move.LEFT),
#     ((4, 0), Move.TOP),
#     ((4, 0), Move.RIGHT),
#     ((4, 4), Move.TOP),
#     ((4, 4), Move.LEFT),
    
#     # high border moves
#     ((0, 1), Move.BOTTOM),
#     ((0, 2), Move.BOTTOM),
#     ((0, 3), Move.BOTTOM),
#     ((0, 1), Move.RIGHT),
#     ((0, 2), Move.RIGHT),
#     ((0, 3), Move.RIGHT),
#     ((0, 1), Move.LEFT),
#     ((0, 2), Move.LEFT),
#     ((0, 3), Move.LEFT),
    
#     # low border moves
#     ((4, 1), Move.TOP),
#     ((4, 2), Move.TOP),
#     ((4, 3), Move.TOP),
#     ((4, 1), Move.LEFT),
#     ((4, 2), Move.LEFT),
#     ((4, 3), Move.LEFT),
#     ((4, 1), Move.RIGHT),
#     ((4, 2), Move.RIGHT),
#     ((4, 3), Move.RIGHT),
    
#     # left border moves
#     ((1, 0), Move.RIGHT),
#     ((2, 0), Move.RIGHT),
#     ((3, 0), Move.RIGHT),
#     ((1, 0), Move.BOTTOM),
#     ((2, 0), Move.BOTTOM),
#     ((3, 0), Move.BOTTOM),
#     ((1, 0), Move.TOP),
#     ((2, 0), Move.TOP),
#     ((3, 0), Move.TOP),
    
#     # right border moves
#     ((1, 4), Move.LEFT),
#     ((2, 4), Move.LEFT),
#     ((3, 4), Move.LEFT),
#     ((1, 4), Move.TOP),
#     ((2, 4), Move.TOP),
#     ((3, 4), Move.TOP),
#     ((1, 4), Move.BOTTOM),
#     ((2, 4), Move.BOTTOM),
#     ((3, 4), Move.BOTTOM),
#     ]
