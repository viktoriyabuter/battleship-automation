from domain.interfaces.game_ui import GameUI
from domain.strategy.strategy import Strategy
from domain.enums.shot_result import ShotResult
from domain.enums.game_result import GameResult

MAX_TURNS: int = 100


def run_game(ui: GameUI) -> GameResult:

    strategy: Strategy = Strategy(ui)

    for turn in range(MAX_TURNS):
        game_result: GameResult | None = ui.wait_for_game_event()

        if game_result is not None:
            return game_result

        x, y = strategy.choose_next_shot()

        shot_result: ShotResult = ui.shoot(x, y)
        strategy.register_result((x, y), shot_result)

    raise RuntimeError(f"Game did not finish within {MAX_TURNS} turns.")
