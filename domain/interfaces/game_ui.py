from abc import ABC, abstractmethod
from typing import List, Optional
from domain.enums.shot_result import ShotResult
from domain.enums.game_result import GameResult
from domain.models.coordinate import Coordinate


class GameUI(ABC):

    @abstractmethod
    def wait_for_opponent(self) -> None:
        pass

    @abstractmethod
    def wait_for_game_event(self) -> Optional[GameResult]:
        pass

    @abstractmethod
    def get_empty_cells(self) -> List[Coordinate]:
        pass

    @abstractmethod
    def shoot(self, x: int, y: int) -> ShotResult:
        pass

    @abstractmethod
    def get_cell_status(self, x: int, y: int) -> ShotResult:
        pass

    @abstractmethod
    def get_game_result(self) -> Optional[GameResult]:
        pass
