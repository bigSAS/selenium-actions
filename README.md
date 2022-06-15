# Selenium Actions
![example workflow](https://github.com/bigSAS/selenium-actions/actions/workflows/buildmodule.yaml/badge.svg)


PyPI - https://pypi.org/project/selenium-actions/

Simple action framework using selenium 🚀

## Real life examples

* behave - https://github.com/bigSAS/selenium-actions-behave-example
* pytest - todo

## Actions
### Create actions object

```python
from seleniumactions import Actions, FluentFinder

# all timeouts are in seconds
timeouts = {
    "short": 2,
    "medium": 3,
    "long": 5,
    "absurd": 10
}
finder = FluentFinder(
    driver,
    timeouts=timeouts,
    default_timeout=timeouts["medium"]
)
actions = Actions(
    finder,
    wait_for_condition_timeout=15,
    wait_between=0.5
)
```


### Examples

```python
from seleniumactions import Actions, LocatorExists


# locators (tuples)
main_header = ('xpath', '//h1[.="Home"]')
menu = ('id', 'menu')
news_option = ('xpath', '//menu-option[.="News"]')
search_input = ('xpath', '//search-news//input')
form = ('xpath', '//form')

# take some actions 🚀
actions.goto('https://some.site.io')  # open site
actions.wait_for(LocatorExists(main_header))  # wait for condition to be met with default timeout from configuration applied
actions.click(menu)  # default timeout from configuration applied
actions.click(news_option, timeout='medium')  # 'medium' timeout from configuration applied
actions.type_text(search_input, text='python', explicit_timeout=3)  # explicit timeout in seconds (always overrides any timeout from configuration)
actions.submit()  # submit default form (//form) - works when theres only one form on page
# actions.submit(form)  # u can pass form locator also
actions.wait_for(LocatorExists(('xpath', '//search-results')), timeout='long')  # wait for condition with 'long' timeout from configuration applied

# assert ect...
```

## Locators

Lest say we have HTML component (simplified for example 👀)


```html
<ul>
    <li class="menu"> Foo</li>
    <li class="menu"> Bar </li>
    <li class="menu">Baz </li>
</ul>
```

We want to  be able to click each one of them. So the xpath values for them will be:

```python
foo_xpath = "//ul/li[@class='menu' and contains(., 'Foo')]"
bar_xpath = "//ul/li[@class='menu' and contains(., 'Bar')]"
baz_xpath = "//ul/li[@class='menu' and contains(., 'Baz')]"
```

It can be painfull. Of course you can write a function and parametrize the string

```python
def get_menu_xpath(label: str):
    return f"//ul/li[@class='menu' and contains(., '{label}')]"
```

It's kind of frustrating...

We can use Locator class to solve that problem
```python
from seleniumactions import Locator

# You can define any parameters to a locator value template
menu_element = Locator(Using.XPATH, "//ul/li[@class='{class_name}' and contains(., '{label}')]")
menu_element.get_by(class_name='menu', label='Foo')
# >>> ("xpath", "//ul/li[@class='menu' and contains(., 'Foo')]")
menu_element.get_by(class_name='active-menu', label='Bar')
# >>> ("xpath", "//ul/li[@class='active-menu' and contains(., 'Bar')]")

# When you forget to pass values you'll get clear error
button = Locator(Using.NAME, '{action}-{foo}')
button.get_by()
# ValueError: get_by method is missing keyword arguments: ['action', 'foo']
button.get_by(action='goto')
# ValueError: get_by method is missing keyword argument: foo

# cool! 🕹 we can play with it!
```


### Examples (advanced)

We can go step further and implement our own custom locators 🚀
```python
# utils/locators.py
from seleniumactions import Using, Locator


class ButtonByLabel(Locator):
    def __init__(self) -> None:
        super().__init__(Using.XPATH, "//button[.='{label}']")


class ButtonSubmit(Locator):
    def __init__(self) -> None:
        super().__init__(Using.XPATH, "//button[@type='submit']")


class LinkByExactText(Locator):
    def __init__(self) -> None:
        super().__init__(Using.XPATH, "//a[.='{text}']")


class LinkByContainedText(Locator):
    def __init__(self) -> None:
        super().__init__(Using.XPATH, "//a[contains(.='{text}')]")


class HeaderByExactText(Locator):
    def __init__(self) -> None:
        super().__init__(Using.XPATH, "//h*[.='{text}']")


class Locators:
    # for importing and better intellisence in other modules
    link = LinkByExactText()
    link_contains = LinkByContainedText()
    button = ButtonByLabel()
    submit_button = ButtonSubmit()
    header = HeaderByExactText()


###########################################
# test.py
from utlis.locators import Locators as Loc

# raw calling
actions.click(Loc.link.get_by(text='HOME'))
actions.wait_for(Loc.header.get_by(text='Welcome home!'))
actions.click(Loc.link_contains.get_by(text='see more...'))
actions.click(Loc.button.get_by(label='Next'))
actions.click(Loc.submit_button.get_by())

# or for more readability
home_link = Loc.link.get_by(text='HOME')
see_more_link = Loc.link_contains.get_by(text='see more...')
next_button = Loc.button.get_by(label='Next')
submit_button = Loc.submit_button.get_by()
home_header = Loc.header.get_by(text='Welcome home!')

actions.click(home_button)
actions.wait_for(home_header)
actions.click(see_more_link)
actions.click(next_button)
actions.click(submit_button)

# SUPER DRY!
```
