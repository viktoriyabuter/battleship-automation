from application.game_runner import run_game
from domain.enums.game_result import GameResult


def test_battleship_game(battle_page):
    game_result = run_game(battle_page)

    assert (
        game_result == GameResult.WIN
    ), f"Test failed: Game ended with {game_result.name}"
