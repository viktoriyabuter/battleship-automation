from random import choice
from typing import List, Tuple, Optional

from domain.enums.shot_result import ShotResult
from .base_strategy import BaseStrategy

Coordinate = Tuple[int, int]


class ChessboardStrategy(BaseStrategy):
    """
    Стратегия стрельбы по шахматной сетке
    """

    def __init__(self, grid_size: int = 10):
        self.grid_size = grid_size
        self.shots_taken: List[Coordinate] = []
        self.hit_cells: List[Coordinate] = []

    def choose_next_shot(self) -> Coordinate:
        if self.hit_cells:
            next_cell = self._choose_neighbor_cell(self.hit_cells[-1])
            if next_cell:
                return next_cell

        return self._choose_hunt_cell()

    def register_result(self, coord: Coordinate, result: ShotResult) -> None:
        self.shots_taken.append(coord)

        if result == ShotResult.HIT:
            self.hit_cells.append(coord)
        elif result == ShotResult.SUNK:
            self.hit_cells.clear()

    def _choose_hunt_cell(self) -> Coordinate:
        """
        Выбор клетки по шахматному принципу.
        """
        candidates = [
            (x, y)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
            if (x + y) % 2 == 0 and (x, y) not in self.shots_taken
        ]

        if not candidates:
            candidates = [
                (x, y)
                for x in range(self.grid_size)
                for y in range(self.grid_size)
                if (x, y) not in self.shots_taken
            ]

        return choice(candidates)

    def _choose_neighbor_cell(self, coord: Coordinate) -> Optional[Coordinate]:
        x, y = coord

        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

        valid_neighbors = [
            (nx, ny)
            for nx, ny in neighbors
            if 0 <= nx < self.grid_size
            and 0 <= ny < self.grid_size
            and (nx, ny) not in self.shots_taken
        ]

        return choice(valid_neighbors) if valid_neighbors else None
