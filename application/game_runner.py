from domain.strategy.strategy import Strategy
from infrastructure.ui.playwright.pages.battle_page import BattlePage


def run_game(ui: BattlePage):

    strategy = Strategy(ui)

    ui.wait_for_opponent()
    ui.wait_for_your_turn()

    while not ui.get_game_result():
        x, y = strategy.choose_next_shot()

        print(f"Shooting at: ({x},{y})")

        result = ui.shoot(x, y)

        if result is None:
            raise RuntimeError("Shoot returned None")
        print(f"Result: {result.name}")
        strategy.register_result((x, y), result)

        if ui.get_game_result():
            break

        ui.wait_for_your_turn()

    print("Game finished")
