from lucy.config import config, Website
from lucy.scraper import Scraper
from lucy.utils import Token


class Auth:  # pylint: disable=too-few-public-methods

    @staticmethod
    def __login_atcoder() -> None:
        website_config = config.website[Website.ATCODER]

        scraper = Scraper()
        scraper.driver.get(website_config.login_url)
        assert website_config.user_id
        assert website_config.passwd
        scraper.driver.find_element(value='username').send_keys(website_config.user_id)
        scraper.driver.find_element(value='password').send_keys(website_config.passwd)
        scraper.driver.find_element(value='submit').click()
        token_cookie = scraper.driver.get_cookie(website_config.auth_token_name)
        assert token_cookie
        token = Token.encode(token_cookie['value'])
        config.user_cfg.set(f'{Website.ATCODER}.Token', token)

    @staticmethod
    def login(website: Website) -> None:
        if website == Website.ATCODER:
            Auth.__login_atcoder()
