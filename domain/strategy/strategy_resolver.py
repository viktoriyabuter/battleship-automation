from .base_strategy import BaseStrategy
from .chessboard_strategy import ChessboardStrategy
from .target_strategy import TargetStrategy  # если есть
from .probability_strategy import ProbabilityStrategy  # опционально

class StrategyResolver:
    """
    Определяет, какую стратегию использовать для следующего хода.
    """

    def __init__(self):
        self.chessboard_strategy = ChessboardStrategy()
        self.target_strategy = TargetStrategy()  # режим добивания
        self.probability_strategy = ProbabilityStrategy()  # продвинутая стратегия

    def get_strategy(self) -> BaseStrategy:
        """
        Выбирает стратегию на основе текущего состояния.
        Логика:
        - Если есть попадания → target_strategy
        - Иначе → chessboard_strategy
        """
        if self.chessboard_strategy.hit_cells:
            return self.target_strategy
        return self.chessboard_strategy
