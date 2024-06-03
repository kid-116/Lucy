import os

from click.testing import CliRunner
import pytest

from lucy.config import config, ConfigClass, Website
from lucy.main import login
from lucy.scraper import Scraper
from lucy.utils import Token


@pytest.mark.parametrize('website', [Website.ATCODER])
def test_login(runner: CliRunner, website: Website) -> None:
    config.website[website].user_id = os.getenv(f'{str(website).upper()}_USER_ID')
    config.website[website].passwd = os.getenv(f'{str(website).upper()}_PASSWORD')

    website_config = config.website[website]
    result = runner.invoke(login, [str(website)])
    assert result.exit_code == 0
    assert 'Success!' in result.output

    scraper = Scraper()
    scraper.driver.get(website_config.host)
    token = ConfigClass().website[website].token
    assert token
    token = Token.decode(token)
    scraper.driver.add_cookie({'name': website_config.auth_token_name, 'value': token})
    scraper.get(f'{website_config.host}/settings')
    assert 'login' not in scraper.driver.current_url
