import logging, json
from pytest import fixture
from selenium.webdriver.chrome.webdriver import WebDriver as Chromedriver
from selenium.webdriver.chrome.service import Service as ChromeService
log = logging.getLogger(__name__)


@fixture
def store():
    store = dict()
    log.info('yielding store')
    yield store

    log.info('after yielding store')
    store


@fixture(scope="session")
def config():
    # ! this can be loaded from file/api/ect
    static_config = {
        "chromedriver_path": "/Users/omni/code/webdrivers/chrome/102/chromedriver",
        "finder.find_element_timeout_sec": 5,
        "actions.wait_for_condition_timeout_sec": 10,
        "actions.wait_between_actions_sec": 0.5,
    }
    confjson = json.dumps(static_config, indent=2)
    logging.info(f"[webdriver]config -> {confjson}")
    return static_config


@fixture
def chromedriver(config):
    chromeservice = ChromeService(executable_path=config["chromedriver_path"])
    chromedriver = Chromedriver(service=chromeservice)
    yield chromedriver

    chromedriver.quit()


@fixture
def actions(chromedriver, config):
    from seleniumactions import FluentFinder, Actions
    ffinder = FluentFinder(
        webdriver=chromedriver,
        default_timeout=config["finder.find_element_timeout_sec"]
    )
    actions = Actions(
        finder=ffinder,
        wait_for_condition_timeout=config["actions.wait_for_condition_timeout_sec"],
        wait_between=config["actions.wait_between_actions_sec"]
    )
    return actions
