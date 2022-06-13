from selenium.webdriver.remote.webdriver import WebDriver
from seleniumactions import Actions, Locator, Using, assert_condition, LocatorExists, XpathExists



class Loc:
    ANCHOR_BY_LABEL = Locator(Using.XPATH, "//a[.='{label}']")


def test_saskodzi(actions: Actions):
    actions.goto("https://saskodzi.pl")
    actions.click(Loc.ANCHOR_BY_LABEL.get_by(label='Blog'))
    actions.wait_for(XpathExists("//div[@class='blog-list__container']"))

    posts = actions.finder.find_elements((Using.CSS, ".blog-post__link"))
    assert len(posts) > 0


def test_gsearch(actions: Actions):
    actions.goto("https://google.pl")
    query_input = Locator(Using.NAME, 'q')
    cookie_consent = Locator(Using.XPATH, "//div[.='I agree']")
    actions.click(cookie_consent.get_by())
    actions.type_text(query_input.get_by(), text="saskodzi", text_mask="***")
    actions.submit(sleep_after=False)
    actions.sleep(2.5)

    # ! variant 1 - locator + LocatoExists
    # url_saskodzi = Locator(Using.XPATH, "//*[contains(@href,'https://saskodzi.pl')]")
    # url_saskodzi_is_present = LocatorExists(url_saskodzi.get_by())

    # ! variant 2 - custom class
    class SaskodziUrlExists(XpathExists):
        def __init__(self): super().__init__("//*[contains(@href,'https://saskodzi.pl')]")

    assert_condition(
        actions,
        condition=SaskodziUrlExists(),
        timeout_sec=3,
        message="Link do saskodzi.pl nie znaleziony..."
    )

    # ! znalesc i zrobic todosy
    # ! POP example
    # ! napisac ladne readme
    # ! opublikowac (pomyslec nad cooler name ? 👀)
