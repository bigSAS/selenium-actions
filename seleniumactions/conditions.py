"""
Expected conditions:

To implement your own expected condition, selenium expects from you object with a __call__ implementation.
Its good to remembet that selenium allways pasess WebDriver instance into __call__ method :)
"""
from selenium.webdriver.remote.webdriver import WebDriver


class LocatorExists:
    """
    Wait for Locator to exist
    """
    def __init__(self, locator_tuple: tuple):
        self.locator_tuple = locator_tuple

    # noinspection PyBroadException
    def __call__(self, driver: WebDriver):
        try:
            driver.find_element(*self.locator_tuple)
            return True
        except Exception:
            return False

    def __str__(self):
        return f'locator exists -> {self.locator_tuple}'

    def __repr__(self):
        return self.__str__()
