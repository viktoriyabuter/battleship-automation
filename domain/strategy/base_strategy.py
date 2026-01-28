from abc import ABC, abstractmethod
from typing import Tuple
from domain.enums.shot_result import ShotResult

Coordinate = Tuple[int, int]


class BaseStrategy(ABC):

    @abstractmethod
    def choose_next_shot(self) -> Coordinate:
        pass

    @abstractmethod
    def register_result(self, coord: Coordinate, result: ShotResult) -> None:
        pass
