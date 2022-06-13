import logging, sys
from time import sleep, time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from seleniumactions.elements import Finder


logger = logging.getLogger('ACTIONS')
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


def time_it(f):
    """
    Mesure execution in seconds
    """
    def wrapper(*args, **kwargs):
        begin = time()
        result = f(*args, **kwargs)
        end = time()
        logger.info(f'({f.__name__} ^) took {str(round((end - begin), 3))} seconds.')
        return result
    return wrapper


class Actions:
    """
    Action - responsible for webdriver operations:
    - finding elements
    - clicking, typing, submiting etc...

    Parameters:
    finder:  abs.elements.Finder instance (u can use abs.elements.FluentFinder or implement your own :) )
    wait_for_condition_timeout: default wait for condition timeout when using wait_for method
    wait_between: default delay between action method calls, defaults 0sec

    WebDriver and Finder are accessible with properties .webdriver and .finder

    Action methods are preety self explanotary :)
    Most action methods can override timeout (find WebElement timeout)
       and condition (expected condition for finding WebElement).
    For readability purpouses they should be used as keyword arguments(timeout)

    Example usage:
    finder = FluenFinder(webdriver, default_timeout=5)
    actions = Actions(finder, wait_for_condition_timeout=10, wait_between=1)

    actions.goto(url)
    actions.click(locator)
    actions.click(locator, timeout=10)


    For more practical examples check out README.md / docs

    The actions.<method>(locator_tuple: tuple) ->
       classic tuple for selenium webriver methods ex: ('xpath', '//div/form') or ('id', 'foobar')

    For helpful and super handy selector tuple implementation check out abs.elements.Locator documentation :)
    """

    # ! todo: finish docstrings
    def __init__(self, finder: Finder, wait_for_condition_timeout: int, wait_between: int = 0) -> None:
        self.wait_between_sec = wait_between
        self.wait_for_condition_timeout = wait_for_condition_timeout
        self.__finder = finder

    @property
    def webdriver(self) -> WebDriver:
        """
        WebDriver instance used by actions.
        """
        return self.finder.webdriver

    @property
    def finder(self) -> Finder:
        """
        Finder instance used by actions.
        """
        return self.__finder

    @time_it
    def goto(self, url: str) -> None:
        """
        Go to url.
        """
        logger.info(f'goto {url}')
        self.webdriver.get(url)

    @time_it
    def click(self, locator_tuple: tuple,
              timeout: str = None, explicit_timeout: int = None, sleep_after: bool = True) -> None:
        """
        Clik element using locator.

        Examples:
          home_button = ("id", "home-button")
          actions.click(home_button)
          actions.click(home_button, timeout="medium")  # custom timeout finding el to click
          actions.click(home_button, explicit_timeout=15)  # custom explici timeout (seconds) finding el to click
          actions.click(home_button, sleep_after=False)  # no delay after clicking
        """
        logger.info(f'click {locator_tuple}')
        self.finder.find_element(locator_tuple, timeout=timeout, explicit_timeout=explicit_timeout).click()
        if sleep_after: self.sleep()

    @time_it
    def type_text(self, locator_tuple: tuple, text: str, timeout: str = None, explicit_timeout: int = None,
                  sleep_after: bool = True, text_mask: str = None) -> None:
        """
        Type text into element using locator.

        Examples:
          email_input = ("name", "email")
          actions.type_text(email_input, "jimmy@choo.io")
          actions.type_text(email_input, text="jimmy@choo.io", timeout="absurd")  # custom timeout finding el to click
          actions.type_text(email_input, text="jimmy@choo.io", explicit_timeout="absurd")  # custom explicit timeout
          actions.type_text(email_input, text="jimmy@choo.io", sleep_after=False)  # no delay after typing
        """
        tekzt = text_mask or text
        logger.info(f'type text {locator_tuple} : {tekzt}')
        self.finder.find_element(locator_tuple, timeout=timeout, explicit_timeout=explicit_timeout).send_keys(text)
        if sleep_after: self.sleep()

    @time_it
    def clear(self, locator_tuple: tuple,
              timeout: str = None, explicit_timeout: int = None, sleep_after: bool = True) -> None:
        """
        Clear element using locator.

        Examples:
          email_input = ("name", "email")
          actions.clear(email_input)
          actions.clear(email_input, timeout="short")  # custom timeout finding el to click
          actions.clear(email_input, explicit_timeout=15)  # custom explicit timeout (seconds) finding el to click
          actions.clear(email_input, sleep_after=False)  # no delay after clicking
        """
        logger.info(f'clear field {locator_tuple}')
        self.finder.find_element(locator_tuple, timeout=timeout, explicit_timeout=explicit_timeout).clear()
        if sleep_after: self.sleep()

    @time_it
    def submit(self, locator_tuple: tuple = None,
               timeout: str = None, explicit_timeout: int = None, sleep_after: bool = True) -> None:
        """
        Submit form.

        Examples:
          actions.submit()  # only one form on page
          account_form = ("id", "account-form")
          actions.submit(account_form)
          actions.submit(account_form, timeout="medium")  # custom timeout finding el to click
          actions.submit(account_form, explicit_timeout=20)  # custom explicit timeout (seconds) finding el to click
          actions.submit(account_form, sleep_after=False)  # no delay after clicking
        """
        lt = locator_tuple if locator_tuple else ('xpath', '//form')
        logger.info(f'submit {lt}')
        self.finder.find_element(lt, timeout=timeout, explicit_timeout=explicit_timeout).submit()
        if sleep_after: self.sleep()

    @time_it
    def wait_for(self, condition: object, timeout: str = None, explicit_timeout: int = None) -> None:
        """
        Wait for expected condition to be met.

        Examples:
          condition = LocatorExists(("id", "home"))
          actions.wait_for(condition)
          actions.wait_for(condition, explicit_timeout=50)  # custom explicit timeout (seconds)
        """
        t = self.wait_for_condition_timeout
        if timeout is not None:
            try:
                t = self.finder.timeouts[timeout.lower()]
            except KeyError:
                valid_options = list(self.finder.timeouts.keys())
                raise ValueError(f'Invalid timeout variant: "{timeout}", use {valid_options}')
        if explicit_timeout is not None: t = explicit_timeout
        logger.info(f'wait for {condition}, timeout: {t} sec')
        WebDriverWait(self.webdriver, t).until(condition)

    @time_it
    def get_attribute(self, locator_tuple: tuple, attr: str, timeout: str = None, explicit_timeout: int = None) -> str:
        logger.info(f'get attribute {locator_tuple} [{attr}]')
        return self.finder.find_element(locator_tuple, timeout=timeout, explicit_timeout=explicit_timeout)\
            .get_attribute(attr)

    @time_it
    def get_text(self, locator_tuple: tuple, timeout: str = None, explicit_timeout: int = None) -> str:
        return self.get_attribute(locator_tuple, 'innerText', timeout=timeout, explicit_timeout=explicit_timeout)

    @time_it
    def execute_js(self, js_script: str) -> str:
        logger.info(f'execute js\n{js_script}')
        return str(self.webdriver.execute_script(js_script))

    @time_it
    def hover(self, locator_tuple: tuple,
              timeout: str = None, explicit_timeout: int = None, sleep_after: bool = True) -> None:
        logger.info(f'hover element {locator_tuple}')
        element = self.finder.find_element(locator_tuple, timeout=timeout, explicit_timeout=explicit_timeout)
        ActionChains(self.webdriver).move_to_element(element).perform()
        if sleep_after: self.sleep()

    def sleep(self, sec: int = None):
        seconds = sec if sec else self.wait_between_sec
        logger.info(f'sleep {seconds} sec')
        sleep(seconds)
