import random
from typing import List, Optional, Set, Tuple

from domain.enums.shot_result import ShotResult
from domain.interfaces.game_ui import GameUI
from domain.models.coordinate import Coordinate
from domain.strategy.base_strategy import BaseStrategy


class Strategy(BaseStrategy):

    def __init__(self, page: GameUI) -> None:
        self.page: GameUI = page
        self.current_hits: List[Coordinate] = []
        self.shots: Set[Coordinate] = set()

    def choose_next_shot(self) -> Coordinate:
        empty_cells: List[Coordinate] = self.page.get_empty_cells()
        empty_set: Set[Coordinate] = set(empty_cells) - self.shots

        if self.current_hits:
            target: Optional[Coordinate] = self._target_mode(empty_set)
            if target:
                self.shots.add(target)
                return target

        target = self._hunt_mode(empty_set)
        self.shots.add(target)
        return target

    def _hunt_mode(self, empty_set: Set[Coordinate]) -> Coordinate:
        """Режим поиска корабля — шахматный узор"""
        chess_cells: List[Coordinate] = [c for c in empty_set if (c[0] + c[1]) % 2 == 0]
        if chess_cells:
            return random.choice(chess_cells)
        return random.choice(list(empty_set))

    def _target_mode(self, empty_set: Set[Coordinate]) -> Optional[Coordinate]:
        """Режим добивания корабля после попаданий"""
        if len(self.current_hits) == 1:
            x, y = self.current_hits[0]
            neighbors: List[Coordinate] = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]
            valid: List[Coordinate] = [c for c in neighbors if c in empty_set]
            if valid:
                return random.choice(valid)
            return None

        xs: Set[int] = {c[0] for c in self.current_hits}
        ys: Set[int] = {c[1] for c in self.current_hits}

        if len(xs) == 1:
            x: int = xs.pop()
            sorted_hits: List[Coordinate] = sorted(
                self.current_hits, key=lambda c: c[1]
            )
            for candidate_y in [sorted_hits[0][1] - 1, sorted_hits[-1][1] + 1]:
                candidate: Coordinate = (x, candidate_y)
                if candidate in empty_set:
                    return candidate

        if len(ys) == 1:
            y: int = ys.pop()
            sorted_hits = sorted(self.current_hits, key=lambda c: c[0])
            for candidate_x in [sorted_hits[0][0] - 1, sorted_hits[-1][0] + 1]:
                candidate: Coordinate = (candidate_x, y)
                if candidate in empty_set:
                    return candidate

        return None

    def process_result(self, coord: Coordinate, result: ShotResult) -> None:
        if result == ShotResult.HIT:
            self.current_hits.append(coord)
        elif result == ShotResult.SUNK:
            self.current_hits.clear()

    def register_result(self, coord: Coordinate, result: ShotResult) -> None:
        self.process_result(coord, result)
