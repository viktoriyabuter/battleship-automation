import random
from typing import List, Optional, Set

from domain.enums.shot_result import ShotResult
from domain.models.coordinate import Coordinate
from domain.strategy.base_strategy import BaseStrategy


class Strategy(BaseStrategy):

    def __init__(self, page):
        self.page = page
        self.current_hits: List[Coordinate] = []
        self.shots: Set[Coordinate] = set()

    def choose_next_shot(self) -> Coordinate:
        empty_cells = self.page.get_empty_cells()
        empty_set = set(empty_cells)

        if self.current_hits:
            target = self._target_mode(empty_set)
            if target:
                self.shots.add(target)
                return target

        target = self._hunt_mode(empty_cells)

        self.shots.add(target)
        return target

    def _hunt_mode(self, empty_cells: List[Coordinate]) -> Coordinate:
        chess_cells = [c for c in empty_cells if (c[0] + c[1]) % 2 == 0]
        if chess_cells:
            return random.choice(chess_cells)

        return random.choice(empty_cells)

    def _target_mode(self, empty_set: Set[Coordinate]) -> Optional[Coordinate]:
        if len(self.current_hits) == 1:
            x, y = self.current_hits[0]
            neighbors = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]
            valid = [c for c in neighbors if c in empty_set]
            if valid:
                return random.choice(valid)

            return None

        xs = {c[0] for c in self.current_hits}
        ys = {c[1] for c in self.current_hits}

        if len(xs) == 1:

            x = xs.pop()
            sorted_hits = sorted(self.current_hits, key=lambda c: c[1])

            top = (x, sorted_hits[0][1] - 1)
            bottom = (x, sorted_hits[-1][1] + 1)

            for candidate in [top, bottom]:
                if candidate in empty_set:
                    return candidate

        if len(ys) == 1:

            y = ys.pop()
            sorted_hits = sorted(self.current_hits, key=lambda c: c[0])

            left = (sorted_hits[0][0] - 1, y)
            right = (sorted_hits[-1][0] + 1, y)

            for candidate in [left, right]:
                if candidate in empty_set:
                    return candidate

        return None

    def process_result(self, coord: Coordinate, result: str):
        if result == ShotResult.HIT:
            self.current_hits.append(coord)
        elif result == ShotResult.SUNK:
            self.current_hits.clear()

    def register_result(self, coord: Coordinate, result: str):
        result = result.lower().strip()
        valid_results = {ShotResult.HIT, ShotResult.MISS, ShotResult.SUNK}
        if result not in valid_results:
            raise ValueError(f"Unknown shot result: {result}")

        self.process_result(coord, result)
