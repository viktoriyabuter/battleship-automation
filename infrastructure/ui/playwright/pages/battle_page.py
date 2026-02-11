from typing import List
from playwright.sync_api import Page

from config import settings
from domain.enums.game_result import GameResult
from domain.enums.shot_result import ShotResult
from domain.models.coordinate import Coordinate


class BattlePage:
    MOVE_OFF_NOTIFICATION = "div.notification__move-off:not(.none)"
    MOVE_ON_NOTIFICATION = (
        "div.notification__move-on:not(.none), "
        "div.notification__game-started-move-on:not(.none)"
    )
    RIVAL_EMPTY_CELLS = (
        ".battlefield.battlefield__rival "
        ".battlefield-cell__empty .battlefield-cell-content"
    )
    EMPTY_CELL_SELECTOR_TEMPLATE = (
        ".battlefield.battlefield__rival "
        ".battlefield-cell__empty "
        ".battlefield-cell-content[data-x='{x}'][data-y='{y}']"
    )
    LAST_CELL_SELECTOR_TEMPLATE = (
        ".battlefield.battlefield__rival "
        ".battlefield-cell__last "
        ".battlefield-cell-content[data-x='{x}'][data-y='{y}']"
    )
    GAME_OVER_WIN_NOTIFICATION = "div.notification__game-over-win:not(.none)"
    GAME_OVER_LOSE_NOTIFICATION = "div.notification__game-over-lose:not(.none)"
    RIVAL_LEAVE_NOTIFICATION = "div.notification__rival-leave:not(.none)"

    def __init__(self, page: Page):
        self.page = page

    def wait_for_opponent(self) -> None:
        self.page.wait_for_selector(
            f"{self.MOVE_ON_NOTIFICATION}, {self.MOVE_OFF_NOTIFICATION}",
            timeout=settings.WAIT_FOR_OPPONENT_TIMEOUT,
        )

    def wait_for_your_turn(self) -> None:
        self.page.wait_for_selector(
            self.MOVE_ON_NOTIFICATION,
            timeout=settings.WAIT_FOR_TURN_TIMEOUT,
        )

    def get_empty_cells(self) -> List[Coordinate]:
        cells: List[Coordinate] = []
        elements = self.page.locator(self.RIVAL_EMPTY_CELLS).all()
        for el in elements:
            x = int(el.get_attribute("data-x"))
            y = int(el.get_attribute("data-y"))
            cells.append((x, y))

        return cells

    def shoot(self, x: int, y: int) -> ShotResult:
        selector = self.EMPTY_CELL_SELECTOR_TEMPLATE.format(x=x, y=y)
        cell = self.page.locator(selector)
        cell.first.wait_for(state="visible", timeout=5000)
        print(f"Shooting at: ({x},{y})")
        cell.first.click()
        return self._wait_for_result(x, y)

    # ------------------------------------------------

    def _wait_for_result(self, x: int, y: int) -> ShotResult:
        last_cell = self.page.locator(self.LAST_CELL_SELECTOR_TEMPLATE.format(x=x, y=y))
        last_cell.wait_for(state="visible", timeout=10000)
        td = last_cell.locator("..")
        cell_class = td.get_attribute("class") or ""
        if "battlefield-cell__miss" in cell_class:
            return ShotResult.MISS
        if "battlefield-cell__hit" in cell_class:
            if "battlefield-cell__done" in cell_class:
                return ShotResult.SUNK
            return ShotResult.HIT

        raise RuntimeError(f"Unknown result for cell ({x},{y})")

    def get_game_result(self) -> GameResult | None:
        if self.page.locator(self.GAME_OVER_WIN_NOTIFICATION).count():
            return GameResult.WIN
        if self.page.locator(self.GAME_OVER_LOSE_NOTIFICATION).count():
            return GameResult.LOSE
        if self.page.locator(self.RIVAL_LEAVE_NOTIFICATION).count():
            return GameResult.OPPONENT_LEFT

        return None
