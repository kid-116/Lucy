from lucy.auth import Auth
from lucy.config import config, Website
from lucy.scraper import Scraper


def test_login_atcoder() -> None:
    website = Website.ATCODER
    website_config = config.website[website]
    scraper = Scraper()

    scraper.get(website_config.protected_url)

    assert 'login' in scraper.driver.current_url

    Auth.authenticate(scraper, website)

    scraper.get(website_config.protected_url)

    assert 'login' not in scraper.driver.current_url
    username = scraper.driver.find_element(value='ui.UserName')
    assert username.get_attribute('value') == website_config.user_id
