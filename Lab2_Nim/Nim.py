from collections import namedtuple
import logging

Nimply = namedtuple("Nimply", "row, num_objects")

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects
        
    def play(strategies, log=False):
        if log: logging.getLogger().setLevel(logging.INFO)
        nim = Nim(5)
        if log: logging.info(f"init : {nim}")
        player = 0
        while nim:
            ply = strategies[player](nim)
            if log: logging.info(f"ply: player {player} plays {ply}")
            nim.nimming(ply)
            if log: logging.info(f"status: {nim}")
            player = 1 - player
        if log: logging.info(f"status: Player {player} won!")
        return player