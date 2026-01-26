from abc import ABC, abstractmethod
from domain.enums.shot_result import ShotResult


class BattleUIPort(ABC):
    @abstractmethod
    def open_game(self) -> None:
        pass

    @abstractmethod
    def choose_random_opponent(self) -> None:
        pass

    @abstractmethod
    def randomize_ships(self, times: int) -> None:
        pass

    @abstractmethod
    def start_game(self) -> None:
        pass

    @abstractmethod
    def wait_for_opponent(self, timeout: int = 60) -> None:
        pass

    @abstractmethod
    def shoot(self, x: int, y: int) -> ShotResult:
        pass

    @abstractmethod
    def get_game_state_snapshot(self) -> dict:
        pass
