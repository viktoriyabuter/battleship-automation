from playwright.sync_api import sync_playwright
from config.settings import BASE_URL
from infrastructure.ui.playwright.pages.start_page import StartPage
from infrastructure.ui.playwright.pages.placement_page import PlacementPage
from infrastructure.ui.playwright.pages.battle_page import BattlePage
from application.game_runner import run_game


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(BASE_URL)

        start_page = StartPage(page)
        start_page.random_place_ships()
        start_page.select_random_opponent()
        start_page.start_game()

        placement_page = PlacementPage(page)
        placement_page.confirm_placement()  # просто заглушка

        battle_page = BattlePage(page)
        run_game(battle_page)

        browser.close()


if __name__ == "__main__":
    main()
