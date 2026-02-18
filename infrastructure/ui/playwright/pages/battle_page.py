from typing import List, Optional
from domain.enums.shot_result import ShotResult
from domain.enums.game_result import GameResult
from domain.models.coordinate import Coordinate
from config.settings import settings
from domain.interfaces.game_ui import GameUI
from infrastructure.ui.playwright.pages.base_page import BasePage


class BattlePage(BasePage, GameUI):
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
        "server_error": "div.notification__server-error:not(.none)",
    }
    RIVAL_EMPTY_CELLS = f"{RIVAL_BATTLEFIELD} {EMPTY_CELL} {CELL_CONTENT}"

    CELL_RESULT_CLASSES = {
        ShotResult.MISS: "battlefield-cell__miss",
        ShotResult.HIT: "battlefield-cell__hit",
        ShotResult.SUNK: "battlefield-cell__done",
    }

    def wait_for_opponent(self) -> None:
        self._wait_for_selector(
            f"{self.MOVE_NOTIFICATION['on']}, {self.MOVE_NOTIFICATION['off']}",
            timeout=settings.WAIT_FOR_OPPONENT_TIMEOUT,
        )

    def wait_for_game_event(self) -> Optional[GameResult]:
        selector = ", ".join(
            [self.MOVE_NOTIFICATION["on"], *self.GAME_OVER_NOTIFICATION.values()]
        )
        self._wait_for_selector(selector, timeout=settings.WAIT_FOR_TURN_TIMEOUT)
        return self.get_game_result()

    def get_empty_cells(self) -> List[Coordinate]:
        elements = self._get_elements(self.RIVAL_EMPTY_CELLS)
        return [
            (int(el.get_attribute("data-x")), int(el.get_attribute("data-y")))
            for el in elements
        ]

    def shoot(self, x: int, y: int) -> ShotResult:
        selector = self.EMPTY_CELL_SELECTOR_TEMPLATE.format(x=x, y=y)
        self._click(selector)
        return self.get_cell_status(x, y)

    def get_cell_status(self, x: int, y: int) -> ShotResult:
        last_cell = self._get_element(self.LAST_CELL_SELECTOR_TEMPLATE.format(x=x, y=y))
        last_cell.wait_for(state="visible")
        td = last_cell.locator("..")
        cell_class = td.get_attribute("class") or ""

        if self.CELL_RESULT_CLASSES[ShotResult.HIT] in cell_class:
            if self.CELL_RESULT_CLASSES[ShotResult.SUNK] in cell_class:
                return ShotResult.SUNK
            return ShotResult.HIT

        if self.CELL_RESULT_CLASSES[ShotResult.MISS] in cell_class:
            return ShotResult.MISS

        raise RuntimeError(f"Unknown result for cell ({x},{y})")

    def get_game_result(self) -> Optional[GameResult]:
        for key, value in self.GAME_OVER_NOTIFICATION.items():
            if self.page.locator(value).count():
                return getattr(GameResult, key.upper())
        return None
