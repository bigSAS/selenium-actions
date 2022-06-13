import logging, sys
from abc import ABC
from seleniumactions.actions import Actions


logger = logging.getLogger('abs-page')
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class Page(ABC):
    """
    Page Object / Component base abstraction
    It exposes Actions instance with .actions property

    Example usage:

    class SasKodzi(Page):
        url = 'https://sas-kodzi.pl'

        BLOG_BUTTON = Locator(Using.XPATH, '//a[@href="/blog"]')

        def goto_posts(self) -> None:
            self.actions.click(self.BLOG_BUTTON.get_by())
            self.actions.wait_for(XpathExists('//body'))
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
        uri = url if url else self.url
        self.actions.goto(uri)
