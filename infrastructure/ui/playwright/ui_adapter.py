from playwright.sync_api import Page, TimeoutError
from domain.ports.battle_ui_port import BattleUIPort
from domain.enums.shot_result import ShotResult
import config.settings as settings


class PlaywrightBattleUIAdapter(BattleUIPort):
    def __init__(self, page: Page):
        self.page = page

    def open_game(self) -> None:
        self.page.goto(settings.BASE_URL)
        self.page.wait_for_load_state("networkidle")

    def choose_random_opponent(self) -> None:
        self.page.get_by_text(settings.BUTTON["random_opponent"]).click()

    def randomize_ships(self, times: int) -> None:
        button = self.page.get_by_text(settings.BUTTON["randomize_ships"])
        for _ in range(times):
            button.click()

    def start_game(self) -> None:
        self.page.get_by_text(settings.BUTTON["start_game"]).click()

    def wait_for_opponent(self, timeout: int = settings.WAIT_FOR_OPPONENT_TIMEOUT):
        self.page.wait_for_selector(
            f"text={settings.TEXT['your_turn']}",
            timeout=timeout,
        )

    def wait_for_your_turn(self) -> None:
        self.page.wait_for_selector(
            f"text={settings.TEXT['your_turn']}",
            timeout=settings.WAIT_FOR_TURN_TIMEOUT,
        )

    def shoot(self, x: int, y: int) -> ShotResult:
        cell_selector = settings.CELL_SELECTOR.format(x=x, y=y)
        cell = self.page.locator(cell_selector)

        cell.click()

        try:
            self.page.wait_for_selector(
                f"text={settings.TEXT['opponent_turn']}",
                timeout=settings.WAIT_FOR_TURN_TIMEOUT,
            )
        except TimeoutError:
            pass

        cell_class = cell.get_attribute("class") or ""

        if "hit" in cell_class:
            return ShotResult.HIT
        if "sunk" in cell_class:
            return ShotResult.SUNK
        return ShotResult.MISS

    def get_game_state_snapshot(self) -> dict:
        snapshot = {}

        cells = self.page.locator(settings.ALL_CELLS_SELECTOR).all()
        for cell in cells:
            x = cell.get_attribute("data-x")
            y = cell.get_attribute("data-y")
            state = cell.get_attribute("class")
            snapshot[f"{x},{y}"] = state

        return snapshot
