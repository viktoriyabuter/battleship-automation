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
    FIELD_SELECTOR = ".battlefield.battlefield__rival"
    LAST_SHOT_CELL = f"{FIELD_SELECTOR} .battlefield-cell__last"

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
        return self._wait_for_cell_state_change()

    def _get_cell(self, x: int, y: int) -> Locator:
        return self.page.locator(self.CELL_SELECTOR_OPPONENT.format(x=x, y=y))

    def _wait_for_cell_state_change(self) -> ShotResult:
        try:
            last_cell_td = self.page.wait_for_selector(
                self.LAST_SHOT_CELL, timeout=settings.WAIT_FOR_TURN_TIMEOUT
            )

            # Берём div внутри td через query_selector
            last_cell_div = last_cell_td.query_selector("div.battlefield-cell-content")
            x_coord = last_cell_div.get_attribute("data-x") if last_cell_div else None
            y_coord = last_cell_div.get_attribute("data-y") if last_cell_div else None
            print(f"Last shot cell coordinates: x={x_coord}, y={y_coord}")

            # Класс td для результата выстрела
            last_cell_class = last_cell_td.get_attribute("class") or ""
            print(f"Last cell classes: {last_cell_class}") # Для отладки

            if "battlefield-cell__miss" in last_cell_class:
                print("Shot result: MISS")
                return ShotResult.MISS
            elif "battlefield-cell__hit" in last_cell_class:
                print("Shot result: HIT")
                return ShotResult.HIT
            else:
                raise RuntimeError("Unknown shot result in last cell")

        except TimeoutError:
            print("Timeout waiting for last cell to update")
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
