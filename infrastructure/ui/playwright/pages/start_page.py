from playwright.sync_api import Page
from config import settings


class StartPage:
    def __init__(self, page: Page):
        self.page = page

    def select_random_opponent(self) -> None:
        self.page.click(f"text={settings.BUTTON['random_opponent']}")

    def start_game(self) -> None:
        self.page.click(f"text={settings.BUTTON['start_game']}")
