from playwright.sync_api import Page


class StartPage:
    RANDOM_OPPONENT_BUTTON = (
        "a.battlefield-start-choose_rival-variant-link:has-text('случайный')"
    )
    START_GAME_BUTTON = "div.battlefield-start-button"

    def __init__(self, page: Page):
        self.page = page

    def select_random_opponent(self) -> None:
        self.page.wait_for_selector(self.RANDOM_OPPONENT_BUTTON, timeout=30_000)
        self.page.click(self.RANDOM_OPPONENT_BUTTON)

    def start_game(self) -> None:
        self.page.wait_for_selector(self.START_GAME_BUTTON, timeout=30_000)
        self.page.click(self.START_GAME_BUTTON)
