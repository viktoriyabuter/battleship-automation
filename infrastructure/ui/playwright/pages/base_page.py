from typing import List, Optional
from playwright.sync_api import Page, Locator


class BasePage:

    def __init__(self, page: Page) -> None:
        self.page: Page = page

    def _wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)

    def _get_element(self, selector: str, timeout: int = 5000) -> Locator:
        self._wait_for_selector(selector, timeout)
        return self.page.locator(selector)

    def _get_elements(self, selector: str, timeout: int = 5000) -> List[Locator]:
        self._wait_for_selector(selector, timeout)
        return self.page.locator(selector).all()

    def _click(
        self,
        selector: str,
        timeout: int = 5000,
        wait_for_selector: Optional[str] = None,
    ) -> None:
        element = self._get_element(selector, timeout)
        element.first.click(timeout=timeout)
        if wait_for_selector:
            self._wait_for_selector(wait_for_selector, timeout)
