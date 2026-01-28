from playwright.sync_api import Page, TimeoutError, Locator

from config import settings
from domain.enums.game_result import GameResult
from domain.enums.shot_result import ShotResult


class BattlePage:
    def __init__(self, page: Page):
        self.page = page

    def wait_for_opponent(self) -> None:
        try:
            self.page.wait_for_selector(
                f"text={settings.TEXT['your_turn']}",
                timeout=settings.WAIT_FOR_OPPONENT_TIMEOUT,
            )
        except TimeoutError as exc:
            raise RuntimeError("Opponent did not connect") from exc

    def wait_for_your_turn(self) -> None:
        self.page.wait_for_selector(
            f"text={settings.TEXT['your_turn']}",
            timeout=settings.WAIT_FOR_TURN_TIMEOUT,
        )

    def get_game_result(self) -> GameResult | None:
        content = self.page.content()

        if settings.TEXT["victory"] in content:
            return GameResult.VICTORY
        if settings.TEXT["defeat"] in content:
            return GameResult.DEFEAT
        if settings.TEXT["opponent_left"] in content:
            return GameResult.OPPONENT_LEFT

        return None

    def wait_for_game_end(self) -> GameResult:
        self.page.wait_for_function(
            """
            (endTexts) => {
                const text = document.body.innerText;
                return endTexts.some(t => text.includes(t));
            }
            """,
            arg=settings.END_GAME_TEXTS,
            timeout=settings.WAIT_FOR_GAME_END_TIMEOUT,
        )

        result = self.get_game_result()
        if result is None:
            raise RuntimeError("Game finished but result was not detected")

        return result

    def shoot(self, x: int, y: int) -> ShotResult:
        cell = self._get_cell(x, y)
        cell.click()

        self._wait_for_cell_state_change(cell)

        classes = cell.get_attribute("class") or ""

        if "hit" in classes:
            return ShotResult.HIT
        if "miss" in classes:
            return ShotResult.MISS

        raise RuntimeError(f"Unknown shot result at ({x}, {y})")

    def _get_cell(self, x: int, y: int) -> Locator:
        return self.page.locator(settings.CELL_SELECTOR.format(x=x, y=y))

    def _wait_for_cell_state_change(self, cell: Locator) -> None:
        self.page.wait_for_function(
            """
            cell =>
                cell.classList.contains('hit') ||
                cell.classList.contains('miss')
            """,
            arg=cell,
            timeout=settings.WAIT_FOR_TURN_TIMEOUT,
        )
