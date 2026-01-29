from enum import Enum


class GameResult(Enum):
    WIN = "win"
    LOSE = "lose"
    OPPONENT_LEFT = "opponent_left"
    CONNECTION_LOST = "connection_lost"
