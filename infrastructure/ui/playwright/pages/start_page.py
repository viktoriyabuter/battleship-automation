import random
from config.settings import settings
from infrastructure.ui.playwright.pages.base_page import BasePage


class StartPage(BasePage):
    RANDOM_OPPONENT_BUTTON = "a.battlefield-start-choose_rival-variant-link"
    START_GAME_BUTTON = "div.battlefield-start-button"
    RANDOM_PLACEMENT_BUTTON = "li.placeships-variant.placeships-variant__randomly"

    def open(self) -> None:
        self.page.goto(settings.BASE_URL)

    def select_random_opponent(self) -> None:
        self._click(self.RANDOM_OPPONENT_BUTTON)

    def start_game(self) -> None:
        self._click(self.START_GAME_BUTTON)

    def random_place_ships(self) -> None:
        num_clicks = random.randint(1, 15)
        self._wait_for_selector(self.RANDOM_PLACEMENT_BUTTON)

        for _ in range(num_clicks):
            self._click(self.RANDOM_PLACEMENT_BUTTON)
            self.page.wait_for_timeout(500)
