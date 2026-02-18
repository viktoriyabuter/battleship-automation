from domain.strategy.strategy import Strategy

MAX_TURNS = 100


def run_game(ui):
    strategy = Strategy(ui)

    for turn in range(MAX_TURNS):
        game_result = ui.wait_for_game_event()

        if game_result is not None:
            return game_result

        x, y = strategy.choose_next_shot()

        shot_result = ui.shoot(x, y)
        strategy.register_result((x, y), shot_result)

    raise RuntimeError(f"Game did not finish within {MAX_TURNS} turns.")
