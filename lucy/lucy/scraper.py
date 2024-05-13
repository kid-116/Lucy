from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions


# pylint: disable=too-few-public-methods
class Scraper:

    def __init__(self) -> None:
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")

        self.driver = Chrome(options=options)

    def get(self, url: str) -> BeautifulSoup:
        status_code = requests.get(url, timeout=100).status_code
        if status_code != 200:
            raise ValueError(f'Failed to get {url}: {status_code}')
        page = None
        self.driver.get(url)
        page = self.driver.page_source
        return BeautifulSoup(page, 'lxml')
