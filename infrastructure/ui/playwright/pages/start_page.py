import random
from playwright.sync_api import Page

from config.settings import settings


class StartPage:
    RANDOM_OPPONENT_BUTTON = (
        "a.battlefield-start-choose_rival-variant-link"
    )
    START_GAME_BUTTON = "div.battlefield-start-button"
    RANDOM_PLACEMENT_BUTTON = "li.placeships-variant.placeships-variant__randomly"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(settings.BASE_URL)

    def select_random_opponent(self) -> None:
        self.page.wait_for_selector(self.RANDOM_OPPONENT_BUTTON, timeout=30_000)
        self.page.click(self.RANDOM_OPPONENT_BUTTON)

    def start_game(self) -> None:
        self.page.wait_for_selector(self.START_GAME_BUTTON, timeout=30_000)
        self.page.click(self.START_GAME_BUTTON)

    def random_place_ships(self) -> None:
        num_clicks = random.randint(1, 15)

        self.page.wait_for_selector(self.RANDOM_PLACEMENT_BUTTON, timeout=10_000)

        for _ in range(num_clicks):
            self.page.click(self.RANDOM_PLACEMENT_BUTTON)
            self.page.wait_for_timeout(500)
