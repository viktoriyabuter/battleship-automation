from playwright.sync_api import sync_playwright
from config.settings import settings
from infrastructure.ui.playwright.pages.start_page import StartPage
from infrastructure.ui.playwright.pages.battle_page import BattlePage
from application.game_runner import run_game


def main():
    with sync_playwright() as pw:
        browser = getattr(pw, settings.BROWSER).launch(
            headless=settings.HEADLESS,
            args=list(settings.BROWSER_ARGS),
            slow_mo=settings.SLOW_MO,
        )
        context = browser.new_context(no_viewport=settings.NO_VIEWPORT)
        page = context.new_page()
        page.goto(settings.BASE_URL)

        start_page = StartPage(page)
        start_page.random_place_ships()
        start_page.select_random_opponent()
        start_page.start_game()

        battle_page = BattlePage(page)
        run_game(battle_page)

        browser.close()


if __name__ == "__main__":
    main()
