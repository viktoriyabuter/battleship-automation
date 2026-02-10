from .base_strategy import BaseStrategy
from .chessboard_strategy import ChessboardStrategy
from .target_strategy import TargetStrategy


class StrategyResolver:
    def __init__(self):
        self.chessboard_strategy = ChessboardStrategy()
        self.target_strategy = TargetStrategy()

    def get_strategy(self) -> BaseStrategy:
        if self.chessboard_strategy.hit_cells:
            return self.target_strategy
        return self.chessboard_strategy
