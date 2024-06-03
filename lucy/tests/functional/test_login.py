import os

from click.testing import CliRunner
import pytest

from lucy.auth import Auth
from lucy.config import config, ConfigClass, Website
from lucy.main import login
from lucy.scraper import Scraper


@pytest.mark.parametrize('website,protected_path', [(Website.ATCODER, 'settings')])
def test_login(runner: CliRunner, website: Website, protected_path: str) -> None:
    config.website[website].user_id = os.getenv(f'{str(website).upper()}_USER_ID')
    config.website[website].passwd = os.getenv(f'{str(website).upper()}_PASSWORD')

    scraper = Scraper()
    website_config = config.website[website]

    scraper.get(f'{website_config.host}/{protected_path}')
    assert 'login' in scraper.driver.current_url

    result = runner.invoke(login, [str(website)])
    assert result.exit_code == 0
    assert 'Success!' in result.output

    config.website[website].token = ConfigClass().website[website].token
    Auth.authenticate(scraper, website)
    scraper.get(f'{website_config.host}/{protected_path}')
    assert 'login' not in scraper.driver.current_url
