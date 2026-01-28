from playwright.sync_api import Page


class PlacementPage:
    def __init__(self, page: Page):
        self.page = page

    def confirm_placement(self) -> None:
        pass
