from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Settings:
    BASE_URL: str = "http://ru.battleship-game.org"

    WAIT_FOR_OPPONENT_TIMEOUT: int = 100_000
    WAIT_FOR_TURN_TIMEOUT: int = 100_000
    WAIT_FOR_GAME_END_TIMEOUT: int = 10_000

    BROWSER: str = "chromium"
    HEADLESS: bool = False
    BROWSER_ARGS: Tuple[str, ...] = ("--start-maximized", )
    SLOW_MO: int = 0

    NO_VIEWPORT: bool = True

    CELL_SELECTOR: str = "[data-x='{x}'][data-y='{y}']"


settings = Settings()
