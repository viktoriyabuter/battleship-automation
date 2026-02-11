from enum import Enum


class GameResult(Enum):
    WIN = "win"
    LOSE = "lose"
    OPPONENT_LEFT = "opponent_left"
    SERVER_ERROR = "server_error"
