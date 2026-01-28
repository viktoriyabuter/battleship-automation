from enum import Enum


class GameResult(Enum):
    VICTORY = "victory"
    DEFEAT = "defeat"
    OPPONENT_LEFT = "opponent_left"
    CONNECTION_LOST = "connection_lost"
