from lucy.browser import Browser
from lucy.config.config import config, Website
from lucy.config.website import Token


class Auth:  # pylint: disable=too-few-public-methods

    @staticmethod
    def __login_atcoder() -> None:
        website_config = config.website[Website.ATCODER]

        browser = Browser()
        browser.driver.get(website_config.login_url)
        assert website_config.user_id
        assert website_config.passwd
        browser.driver.find_element(value='username').send_keys(website_config.user_id)
        browser.driver.find_element(value='password').send_keys(website_config.passwd)
        browser.driver.find_element(value='submit').click()
        if browser.driver.current_url != f'{website_config.host}/home':
            raise ValueError('Invalid credentials.')
        token_cookie = browser.driver.get_cookie(website_config.auth_token_name)
        assert token_cookie
        token = Token(token_cookie['value'])
        config.user_cfg.set(f'{Website.ATCODER}.Token', token)

    @staticmethod
    def login(website: Website) -> None:
        if website == Website.ATCODER:
            Auth.__login_atcoder()
