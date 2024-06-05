from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from lucy.auth import Auth
from lucy.config import config, Website
from lucy.filesystem import LocalFS
from lucy.scraper import Scraper


def submit(website: Website, contest_id: str, task_id: str, hidden: bool) -> None:
    if website == Website.ATCODER:
        scraper = Scraper(headless=hidden, detach=not hidden, maximize=False)
        Auth.authenticate(scraper, website)
        scraper.driver.get(f'{config.website[website].host}/contests/{contest_id}/submit')
        task_selector = Select(scraper.driver.find_element(value='select-task'))
        task_selector.select_by_index(ord(task_id) - ord('A'))
        lang_selector = Select(
            scraper.driver.find_element(by=By.CSS_SELECTOR, value='#select-lang>div>select'))
        lang_selector.select_by_value('5001')
        soln_input = scraper.driver.find_element(by=By.CSS_SELECTOR, value='#editor>textarea')
        soln = LocalFS.read(
            LocalFS.get_impl_path(website=website, contest_id=contest_id, task_id=task_id))
        soln_input.send_keys(soln)
        scraper.driver.find_element(value='submit').click()
        detail_link = scraper.driver.find_element(
            by=By.CSS_SELECTOR, value='table>tbody>tr td:last-of-type a').get_attribute('href')
        assert isinstance(detail_link, str)
        scraper.driver.get(detail_link)
