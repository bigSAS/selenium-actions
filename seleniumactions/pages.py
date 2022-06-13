from abc import ABC
from seleniumactions.actions import Actions


class Page(ABC):
    """
    Page Object / Component base abstraction
    It exposes Actions instance with .actions property

    Example usage:

        from seleniumactions import Page, Using, Locator

        class SasKodzi(Page):
            url = 'https://saskodzi.pl'

            BLOG_BUTTON = Locator(Using.XPATH, '//a[@href="/blog"]').get_by()

            def goto_posts(self) -> None:
                self.actions.click(self.BLOG_BUTTON)

    """

    url = None

    def __init__(self, actions: Actions):
        self.__actions = actions

    @property
    def actions(self) -> Actions:
        return self.__actions

    @property
    def title(self):
        return self.actions.finder.webdriver.title

    def open(self, url: str = None):
        uri = url or self.url
        self.actions.goto(uri)
