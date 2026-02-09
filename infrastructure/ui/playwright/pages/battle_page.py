from playwright.sync_api import Page, Locator, TimeoutError
from config import settings
from domain.enums.game_result import GameResult
from domain.enums.shot_result import ShotResult


class BattlePage:
    MOVE_OFF_NOTIFICATION = "div.notification__move-off:not(.none)"
    MOVE_ON_NOTIFICATION = "div.notification__move-on:not(.none), div.notification__game-started-move-on:not(.none)"
    CELL_SELECTOR_OPPONENT = ".battlefield.battlefield__rival .battlefield-cell-content[data-x='{x}'][data-y='{y}']"
    RIVAL_LEAVE_NOTIFICATION = "div.notification__rival-leave:not(.none)"
    GAME_OVER_WIN_NOTIFICATION = "div.notification__game-over-win:not(.none)"
    GAME_OVER_LOSE_NOTIFICATION = "div.notification__game-over-lose:not(.none)"

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
        """Ждём конца игры, возвращаем результат."""
        self.page.wait_for_selector(
            f"{self.GAME_OVER_WIN_NOTIFICATION},"
            f" {self.GAME_OVER_LOSE_NOTIFICATION},"
            f" {self.RIVAL_LEAVE_NOTIFICATION}",
            timeout=settings.WAIT_FOR_GAME_END_TIMEOUT,
        )

        result = self.get_game_result()
        if result is None:
            raise RuntimeError("Game finished but result was not detected")
        return result

    # --- Определение результата игры через локаторы ---
    def get_game_result(self) -> GameResult | None:
        """Определяем результат игры по видимым нотификациям."""
        if self.page.locator(self.GAME_OVER_WIN_NOTIFICATION).count() > 0:
            return GameResult.WIN
        if self.page.locator(self.GAME_OVER_LOSE_NOTIFICATION).count() > 0:
            return GameResult.LOSE
        if self.page.locator(self.RIVAL_LEAVE_NOTIFICATION).count() > 0:
            return GameResult.OPPONENT_LEFT
        return None

    def shoot(self, x: int, y: int) -> ShotResult:
        cell = self._get_cell(x, y)
        print(f"Shooting at coordinates: x={x}, y={y}")  # Выводим координаты для дебага
        cell.first.click()
        return self._wait_for_cell_to_be_last(x,y)

    def _get_cell(self, x: int, y: int) -> Locator:
        return self.page.locator(self.CELL_SELECTOR_OPPONENT.format(x=x, y=y))

    def _get_last_cell_locator(self, x: int, y: int) -> Locator:
        return self.page.locator(
            f".battlefield.battlefield__rival .battlefield-cell__last .battlefield-cell-content[data-y='{y}'][data-x='{x}']"
        )

    def _wait_for_cell_to_be_last(self, x: int, y: int) -> ShotResult:
        cell_locator = self._get_last_cell_locator(x, y)

        try:
            td_locator = cell_locator.locator("..")  # .. означает родителя в CSS
            print(f"Waiting for td cell to be...{td_locator}")
            # Берём класс родительского td
            cell_class = td_locator.get_attribute("class") or ""
            print(f"Cell ({x},{y}) classes (td): {cell_class}")

            if "battlefield-cell__hit" in cell_class:
                return ShotResult.HIT
            elif "battlefield-cell__miss" in cell_class:
                return ShotResult.MISS
            else:
                raise RuntimeError(f"Unknown shot result in cell ({x},{y})")

        except Exception as e:
            print(f"Error while checking cell ({x},{y}): {e}")
            raise

    def play_turn(self, x: int, y: int) -> ShotResult | None:
        """Полный цикл для хода: проверяем игру, выстрел, ожидание, проверка."""
        # Проверяем, не закончилась ли игра
        game_result = self.get_game_result()
        if game_result is not None:
            print(f"Game finished: {game_result.name}")
            return None  # Игра закончена, ход делать нельзя

        # Совершаем выстрел
        shot_result = self.shoot(x, y)
        print(f"Shot result: {shot_result.name}")

        # Ждём конца хода противника
        self.page.wait_for_selector(
            self.MOVE_OFF_NOTIFICATION, timeout=settings.WAIT_FOR_TURN_TIMEOUT
        )

        # Ждём, когда снова будет наш ход
        self.page.wait_for_selector(
            self.MOVE_ON_NOTIFICATION, timeout=settings.WAIT_FOR_TURN_TIMEOUT
        )

        # Проверяем, не закончилась ли игра после хода противника
        game_result = self.get_game_result()
        if game_result is not None:
            print(f"Game finished: {game_result.name}")

        return shot_result
