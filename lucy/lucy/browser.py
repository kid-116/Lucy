from typing import Optional

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from lucy.config.config import config
from lucy.types import Website


# pylint: disable=too-few-public-methods
class Browser:

    def authenticate(self, website: Website) -> None:
        self.driver.get(config.website[website].host)
        self.driver.add_cookie(config.website[website].cookie)

    def __init__(self,
                 headless: bool = True,
                 detach: bool = False,
                 maximize: bool = True,
                 authenticate: Optional[Website] = None) -> None:
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_experimental_option('detach', detach)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        if maximize:
            options.add_argument('--window-size=1920,1080')

        self.driver = Chrome(options=options)

        if authenticate:
            self.authenticate(authenticate)

    def get_soup(self) -> BeautifulSoup:
        page = self.driver.page_source
        return BeautifulSoup(page, 'lxml')
