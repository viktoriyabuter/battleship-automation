from playwright.sync_api import Page, Locator, TimeoutError
from config import settings
from domain.enums.game_result import GameResult
from domain.enums.shot_result import ShotResult


class BattlePage:
    MOVE_OFF_NOTIFICATION = "div.notification__move-off:not(.none)"
    MOVE_ON_NOTIFICATION = "div.notification__move-on:not(.none), div.notification__game-started-move-on:not(.none)"

    CELL_SELECTOR_OPPONENT = ".battlefield.battlefield__rival .battlefield-cell-content[data-x='{x}'][data-y='{y}']"

    RIVAL_LEAVE_NOTIFICATION = "div.notification__rival-leave:not(.none)"
    END_GAME_TEXTS = settings.END_GAME_TEXTS

    def __init__(self, page: Page):
        self.page = page

    def wait_for_opponent(self) -> None:
        try:
            self.page.wait_for_selector(
                f"{self.MOVE_ON_NOTIFICATION}, {self.MOVE_OFF_NOTIFICATION}",
                timeout=settings.WAIT_FOR_OPPONENT_TIMEOUT,
            )
        except TimeoutError as exc:
            raise RuntimeError("Opponent did not connect / game did not start") from exc

    def wait_for_your_turn(self) -> None:
        self.page.wait_for_selector(
            self.MOVE_ON_NOTIFICATION,
            timeout=settings.WAIT_FOR_TURN_TIMEOUT,
        )

    def wait_for_game_end(self) -> GameResult:
        self.page.wait_for_selector(
            f"{', '.join(self.END_GAME_TEXTS)}, {self.RIVAL_LEAVE_NOTIFICATION}",
            timeout=settings.WAIT_FOR_GAME_END_TIMEOUT,
        )

        result = self.get_game_result()
        if result is None:
            raise RuntimeError("Game finished but result was not detected")
        return result

    def get_game_result(self) -> GameResult | None:
        victory_selector = "div.notification__victory:not(.none)"
        defeat_selector = "div.notification__defeat:not(.none)"
        opponent_left_selector = self.RIVAL_LEAVE_NOTIFICATION

        if self.page.locator(victory_selector).count() > 0:
            return GameResult.VICTORY
        if self.page.locator(defeat_selector).count() > 0:
            return GameResult.DEFEAT
        if self.page.locator(opponent_left_selector).count() > 0:
            return GameResult.OPPONENT_LEFT

        return None

    def shoot(self, x: int, y: int) -> ShotResult:
        """Делаем выстрел по координатам (x, y) и ждём результата."""
        cell = self._get_cell(x, y)
        cell.first.click()

        # Ждём изменения состояния последней клетки
        return self._wait_for_cell_state_change()

    def _get_cell(self, x: int, y: int) -> Locator:
        return self.page.locator(self.CELL_SELECTOR_OPPONENT.format(x=x, y=y))

    def _wait_for_cell_state_change(self) -> ShotResult:
        selector = ".battlefield-cell__last"

        try:
            last_cell = self.page.wait_for_selector(
                selector, timeout=settings.WAIT_FOR_TURN_TIMEOUT
            )

            classes = last_cell.get_attribute("class") or ""

            if "battlefield-cell__miss" in classes:
                print("Shot result: MISS")
                return ShotResult.MISS
            if "battlefield-cell__hit" in classes:
                print("Shot result: HIT")
                return ShotResult.HIT

            raise RuntimeError("Unknown shot result in last cell")

        except TimeoutError:
            print("Timeout waiting for last cell to update")
            raise

    def play_turn(self, x: int, y: int) -> ShotResult:
        shot_result = self.shoot(x, y)

        self.page.wait_for_selector(
            self.MOVE_OFF_NOTIFICATION, timeout=settings.WAIT_FOR_TURN_TIMEOUT
        )

        self.page.wait_for_selector(
            self.MOVE_ON_NOTIFICATION, timeout=settings.WAIT_FOR_TURN_TIMEOUT
        )

        return shot_result
