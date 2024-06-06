import time
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from lucy.config.config import config
from lucy.filesystem import LocalFS
from lucy.types import Website


# pylint: disable=too-few-public-methods
class Browser:

    def authenticate(self, website: Website) -> None:
        self.driver.get(config.website[website].host)
        self.driver.add_cookie(config.website[website].cookie)

    # pylint: disable=too-many-arguments
    def __init__(self,
                 headless: bool = True,
                 detach: bool = False,
                 maximize: bool = True,
                 authenticate: Optional[Website] = None,
                 download_dir: Path = config.tmp_storage_path) -> None:
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_experimental_option('detach', detach)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        if maximize:
            options.add_argument('--window-size=1920,1080')

        prefs = {'download.default_directory': str(download_dir)}
        options.add_experimental_option('prefs', prefs)

        self.driver = Chrome(options=options)

        if authenticate:
            self.authenticate(authenticate)

    def get_soup(self) -> BeautifulSoup:
        page = self.driver.page_source
        return BeautifulSoup(page, 'lxml')

    def wait_get(self,
                 selector_type: str,
                 selector_value: str,
                 timeout: int = 5,
                 poll: int = 1) -> WebElement:
        wait = WebDriverWait(self.driver, timeout, poll_frequency=poll)
        wait.until(lambda browser: browser.find_element(by=selector_type, value=selector_value))
        return self.driver.find_element(by=selector_type, value=selector_value)

    def sleep(self, timeout: int) -> None:
        time.sleep(timeout)

    def read_downloaded(self, filename: str) -> str:
        path = LocalFS.get_tmp_file_path(filename)
        contents = LocalFS.read(path)
        LocalFS.delete(path)
        return contents
