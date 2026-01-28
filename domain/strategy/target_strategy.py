from typing import Tuple
from domain.enums.shot_result import ShotResult
from .base_strategy import BaseStrategy

Coordinate = Tuple[int, int]


class TargetStrategy(BaseStrategy):
    """
    Заглушка для стратегии добивания.
    Пока просто наследуется от BaseStrategy.
    """

    def choose_next_shot(self) -> Coordinate:
        raise NotImplementedError("TargetStrategy пока не реализована")

    def register_result(self, coord: Coordinate, result: ShotResult) -> None:
        pass
