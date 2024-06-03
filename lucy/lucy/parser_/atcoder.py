import concurrent
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from typing import Any, Generator, Optional, Tuple

import click

from lucy import utils
from lucy.config import config, Website
from lucy.scraper import Scraper

from lucy.parser_.parser_ import Parser, Task


class AtCoderParser(Parser):

    @staticmethod
    def __parse_samples(task_page: Any) -> Generator[Tuple[str, str], None, None]:
        for input, output in utils.batched(task_page.select('pre[id]'), 2):
            yield input.text, output.text

    def __parse_tasks(self, row: Any) -> Optional[Task]:
        data = row.find_all('td')
        task_id, task_name = data[0].text, data[1].text

        if self.task_id is not None and task_id != self.task_id:
            return None

        task_path = f'{self.contest_id}_{task_id.lower()}'
        task_page = Scraper().get(f'{self.tasks_page_url}/{task_path}')
        samples = [sample for sample in AtCoderParser.__parse_samples(task_page)]
        click.secho(f'Found {len(samples)} samples for task {task_id}.', fg='green', bold=True)
        task = Task(task_id, task_name, samples)
        return task

    def __init__(self, contest_id: str, task_id: Optional[str], n_threads: int) -> None:
        self.contest_id = contest_id
        self.task_id = task_id

        scraper = Scraper()

        self.tasks_page_url = f'{config.website[Website.ATCODER].host}/contests/{contest_id}/tasks'
        tasks_page = scraper.get(self.tasks_page_url)

        tasks = []
        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            tasks_table = tasks_page.select('table.table tbody tr')
            click.echo(f'Found {len(tasks_table)} tasks.')
            futures = [executor.submit(self.__parse_tasks, row) for row in tasks_table]
            for future in concurrent.futures.as_completed(futures):
                task = future.result()
                if task:
                    tasks.append(task)

        super().__init__(tasks)
