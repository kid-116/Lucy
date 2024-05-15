from typing import Any, Generator, Optional, Tuple

import click

from lucy import utils
from lucy.config import Config, Website
from lucy.scraper import Scraper

from lucy.parser_.parser_ import Parser, Task


class AtCoderParser(Parser):

    @staticmethod
    def __parse_samples(task_page: Any) -> Generator[Tuple[str, str], None, None]:
        for input, output in utils.batched(task_page.select('pre[id]'), 2):
            yield input.text, output.text

    def __parse_tasks(self, page: Any) -> list[Task]:
        tasks: list[Task] = []

        tasks_table = page.select('table.table tbody tr')
        for row in tasks_table:
            data = row.find_all('td')
            task_id, task_name = data[0].text, data[1].text

            if self.task_id is not None and task_id != self.task_id:
                continue

            task_path = f'{self.contest_id}_{task_id.lower()}'
            task_page = Scraper().get(f'{self.tasks_page_url}/{task_path}')
            samples = [sample for sample in AtCoderParser.__parse_samples(task_page)]
            click.secho(f'Found {len(samples)} samples for task {task_id}.', fg='green', bold=True)

            task = Task(task_id, task_name, samples)
            tasks.append(task)

        return tasks

    def __init__(self, contest_id: str, task_id: Optional[str]) -> None:
        self.contest_id = contest_id
        self.task_id = task_id

        scraper = Scraper()

        self.tasks_page_url = f'{Config.WEBSITE_HOST[Website.ATCODER]}/contests/{contest_id}/tasks'
        tasks_page = scraper.get(self.tasks_page_url)

        tasks = self.__parse_tasks(tasks_page)

        super().__init__(tasks)
