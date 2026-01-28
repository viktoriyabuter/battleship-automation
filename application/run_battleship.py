from playwright.sync_api import sync_playwright
from infrastructure.ui.playwright.pages.battle_page import BattlePage
from application.game_runner import run_game
from config.settings import BASE_URL


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(BASE_URL)

        battle_page = BattlePage(page)

        try:
            run_game(battle_page)
        except Exception as e:
            print(f"Ошибка во время игры: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
