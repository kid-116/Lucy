from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from lucy.browser import Browser
from lucy.config.config import config, Website
from lucy.types import Task


class SubmitOps:  # pylint: disable=too-few-public-methods

    def __submit_atcoder(self, task: Task, browser: Browser) -> None:
        browser.driver.get(f'{config.website[task.site].host}/contests/{task.contest_id}/submit')
        task_selector = Select(browser.driver.find_element(value='select-task'))
        task_selector.select_by_index(ord(task.task_id) - ord('A'))
        lang_selector = Select(
            browser.driver.find_element(by=By.CSS_SELECTOR, value='#select-lang>div>select'))
        lang_selector.select_by_value('5001')
        soln_input = browser.driver.find_element(by=By.CSS_SELECTOR, value='#editor>textarea')
        soln = task.impl_path.read_text()
        soln_input.send_keys(soln)
        browser.driver.find_element(value='submit').click()
        detail_link = browser.driver.find_element(
            by=By.CSS_SELECTOR, value='table>tbody>tr td:last-of-type a').get_attribute('href')
        assert isinstance(detail_link, str)
        browser.driver.get(detail_link)

    def submit(self, task: Task, hidden: bool = False) -> None:
        if task.site == Website.ATCODER:
            browser = Browser(headless=hidden,
                              detach=not hidden,
                              maximize=False,
                              authenticate=task.site)
            self.__submit_atcoder(task, browser)
