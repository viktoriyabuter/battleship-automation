from domain.enums.game_result import GameResult
from domain.strategy.strategy import Strategy
from infrastructure.ui.playwright.pages.battle_page import BattlePage


def run_game(ui: BattlePage):
    strategy = Strategy(ui)

    ui.wait_for_opponent()

    while True:
        game_result = ui.get_game_result()
        if game_result:
            break

        try:
            ui.wait_for_your_turn()
        except:
            game_result = ui.get_game_result()
            if game_result:
                break
            else:
                raise

        x, y = strategy.choose_next_shot()
        print(f"Shooting at: ({x},{y})")
        result = ui.shoot(x, y)
        strategy.register_result((x, y), result)

    assert (
        game_result == GameResult.WIN
    ), f"Test failed: Game ended with {game_result.name}"
    print("You won!")
