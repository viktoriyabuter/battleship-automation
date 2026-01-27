BASE_URL = "http://ru.battleship-game.org"

WAIT_FOR_OPPONENT_TIMEOUT = 30_000
WAIT_FOR_TURN_TIMEOUT = 30_000
WAIT_FOR_GAME_END_TIMEOUT = 30_000

TEXT = {
    "your_turn": "Ваш ход",
    "opponent_turn": "Противник ходит",
    "victory": "Поздравляем, вы победили",
    "defeat": "Вы проиграли",
    "opponent_left": "Противник покинул игру",
}

BUTTON = {
    "random_opponent": "Случайный соперник",
    "randomize_ships": "Случайным образом",
    "start_game": "Играть",
}

CELL_SELECTOR = "[data-x='{x}'][data-y='{y}']"
ALL_CELLS_SELECTOR = "[data-x][data-y]"
