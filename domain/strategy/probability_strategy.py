from typing import Tuple
from domain.enums.shot_result import ShotResult
from .base_strategy import BaseStrategy

Coordinate = Tuple[int, int]


class ProbabilityStrategy(BaseStrategy):
    """
    Заглушка для продвинутой стратегии вероятности.
    """

    def choose_next_shot(self) -> Coordinate:
        raise NotImplementedError("ProbabilityStrategy пока не реализована")

    def register_result(self, coord: Coordinate, result: ShotResult) -> None:
        pass
