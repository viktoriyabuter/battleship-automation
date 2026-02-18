import pytest
from playwright.sync_api import sync_playwright

from config.settings import settings
from infrastructure.ui.playwright.pages.battle_page import BattlePage
from infrastructure.ui.playwright.pages.start_page import StartPage


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as pw:
        browser = getattr(pw, settings.BROWSER).launch(
            headless=settings.HEADLESS,
            args=list(settings.BROWSER_ARGS),
            slow_mo=settings.SLOW_MO,
        )
        yield browser


@pytest.fixture(scope="function")
def battle_page(browser):
    context = browser.new_context(no_viewport=settings.NO_VIEWPORT)

    page = context.new_page()

    start_page = StartPage(page)
    start_page.open()
    start_page.random_place_ships()
    start_page.select_random_opponent()
    start_page.start_game()

    battle_page = BattlePage(page)

    yield battle_page

    context.close()
