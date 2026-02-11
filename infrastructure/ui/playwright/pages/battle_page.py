from typing import List
from playwright.sync_api import Page
from domain.enums.shot_result import ShotResult
from domain.enums.game_result import GameResult
from domain.models.coordinate import Coordinate
from config.settings import settings


class BattlePage:
    RIVAL_BATTLEFIELD = ".battlefield.battlefield__rival"
    EMPTY_CELL = ".battlefield-cell__empty"
    LAST_CELL = ".battlefield-cell__last"
    CELL_CONTENT = ".battlefield-cell-content"

    CELL_SELECTOR_TEMPLATE = (
        "{battlefield} {cell_type} {content}[data-x='{x}'][data-y='{y}']"
    )

    EMPTY_CELL_SELECTOR_TEMPLATE = CELL_SELECTOR_TEMPLATE.format(
        battlefield=RIVAL_BATTLEFIELD,
        cell_type=EMPTY_CELL,
        content=CELL_CONTENT,
        x="{x}",
        y="{y}",
    )
    LAST_CELL_SELECTOR_TEMPLATE = CELL_SELECTOR_TEMPLATE.format(
        battlefield=RIVAL_BATTLEFIELD,
        cell_type=LAST_CELL,
        content=CELL_CONTENT,
        x="{x}",
        y="{y}",
    )
    MOVE_NOTIFICATION = {
        "on": "div.notification__move-on:not(.none), div.notification__game-started-move-on:not(.none)",
        "off": "div.notification__move-off:not(.none)",
    }
    GAME_OVER_NOTIFICATION = {
        "win": "div.notification__game-over-win:not(.none)",
        "lose": "div.notification__game-over-lose:not(.none)",
        "opponent_left": "div.notification__rival-leave:not(.none)",
    }
    RIVAL_EMPTY_CELLS = f"{RIVAL_BATTLEFIELD} {EMPTY_CELL} {CELL_CONTENT}"

    def __init__(self, page: Page):
        self.page = page

    def wait_for_opponent(self):
        self.page.wait_for_selector(
            f"{self.MOVE_NOTIFICATION['on']}, {self.MOVE_NOTIFICATION['off']}",
            timeout=settings.WAIT_FOR_OPPONENT_TIMEOUT,
        )

    def wait_for_your_turn(self):
        self.page.wait_for_selector(
            self.MOVE_NOTIFICATION["on"], timeout=settings.WAIT_FOR_TURN_TIMEOUT
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
        if self.page.locator(self.GAME_OVER_NOTIFICATION["win"]).count():
            return GameResult.WIN
        if self.page.locator(self.GAME_OVER_NOTIFICATION["lose"]).count():
            return GameResult.LOSE
        if self.page.locator(self.GAME_OVER_NOTIFICATION["opponent_left"]).count():
            return GameResult.OPPONENT_LEFT
        return None
