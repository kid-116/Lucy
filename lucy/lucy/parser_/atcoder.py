from lucy.config import Config, Website
from lucy.scraper import Scraper

from .parser_ import Parser, Task


class AtCoderParser(Parser):

    def __init__(self, contest_id: str) -> None:
        self.contest_id = contest_id

        scraper = Scraper()

        home_page_url = f'{Config.WEBSITE_HOST[Website.ATCODER]}/contests/{contest_id}/tasks'
        home_page = scraper.get(home_page_url)

        tasks: list[Task] = []

        tasks_table = home_page.select('table.table tbody tr')
        for row in tasks_table:
            data = row.find_all('td')
            task_id, task_name = data[0].text, data[1].text
            task = Task(task_id, task_name)
            tasks.append(task)

        super().__init__(tasks)
