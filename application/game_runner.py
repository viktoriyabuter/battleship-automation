from domain.strategy.strategy_resolver import StrategyResolver
from domain.enums.game_result import GameResult
from domain.enums.shot_result import ShotResult


def run_game(ui):
    ui.wait_for_opponent()

    resolver = StrategyResolver()

    while True:
        strategy = resolver.get_strategy()
        coord = strategy.choose_next_shot()

        result: ShotResult = ui.shoot(*coord)
        strategy.register_result(coord, result)

        game_result: GameResult | None = ui.get_game_result()
        if game_result is not None:
            print(f"Игра завершена: {game_result.name}")
            if game_result != GameResult.VICTORY:
                raise RuntimeError(f"Игра закончилась не победой: {game_result.name}")
