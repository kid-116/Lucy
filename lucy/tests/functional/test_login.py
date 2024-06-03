import os

from click.testing import CliRunner
import pytest

from lucy.auth import Auth
from lucy.config import config, ConfigClass, Website
from lucy.main import login
from lucy.scraper import Scraper


@pytest.fixture(autouse=True, scope='session')
def setup(runner: CliRunner) -> None:
    for website in Website:
        config.website[website].user_id = os.getenv(f'{str(website).upper()}_USER_ID')
        config.website[website].passwd = os.getenv(f'{str(website).upper()}_PASSWORD')

        result = runner.invoke(login, [str(website)])
        assert result.exit_code == 0
        assert 'Success!' in result.output

        config.website[website].token = ConfigClass().website[website].token


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
