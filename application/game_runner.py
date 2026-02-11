from infrastructure.ui.playwright.pages.battle_page import BattlePage
from domain.strategy.strategy import Strategy
from domain.enums.game_result import GameResult
from utils.utils import coord_to_battleship_notation


def run_game(ui: BattlePage):
    strategy = Strategy(ui)

    while True:
        game_result = ui.wait_for_game_event()
        if game_result is not None:
            break

        empty_cells = ui.get_empty_cells()
        if not empty_cells:
            raise RuntimeError("No empty cells left")

        x, y = strategy.choose_next_shot()

        shot_result = ui.shoot(x, y)
        cell_notation = coord_to_battleship_notation((x, y))
        print(f"Shot at {cell_notation}: {shot_result.name}")

        strategy.register_result((x, y), shot_result)

    assert (
        game_result == GameResult.WIN
    ), f"Test failed: game ended with {game_result.name}"
    print("You won!")

    return game_result
