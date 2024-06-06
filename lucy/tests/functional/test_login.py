from lucy.browser import Browser
from lucy.config.config import config, Website


def test_login_atcoder() -> None:
    website = Website.ATCODER
    website_config = config.website[website]
    browser = Browser()

    browser.driver.get(website_config.protected_url)
    assert 'login' in browser.driver.current_url

    browser.authenticate(website)
    browser.driver.get(website_config.protected_url)
    assert 'login' not in browser.driver.current_url
    username = browser.driver.find_element(value='ui.UserName')
    assert username.get_attribute('value') == website_config.user_id
