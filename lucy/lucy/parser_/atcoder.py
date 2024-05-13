import os
from typing import Any

import click

from lucy import utils
from lucy.config import Config, SampleType, Website
from lucy.scraper import Scraper

from .parser_ import Parser, Task


class AtCoderParser(Parser):

    def __parse_samples(self, task_id: str, task_page: Any) -> int:
        num_samples = 0
        for i, (input, output) in enumerate(utils.batched(task_page.select('pre[id]'), 2)):
            num_samples += 1

            in_path = Config.get_sample_path(Website.ATCODER, self.contest_id, task_id,
                                             SampleType.IN, i)
            os.makedirs(os.path.dirname(in_path), exist_ok=True)
            with open(in_path, 'w', encoding='utf-8') as f:
                f.write(input.text)

            out_path = Config.get_sample_path(Website.ATCODER, self.contest_id, task_id,
                                              SampleType.OUT, i)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(output.text)

        return num_samples

    def __parse_tasks(self, page: Any) -> list[Task]:
        tasks: list[Task] = []

        tasks_table = page.select('table.table tbody tr')
        for row in tasks_table:
            data = row.find_all('td')
            task_id, task_name = data[0].text, data[1].text

            task_path = f'{self.contest_id}_{task_id.lower()}'
            task_page = Scraper().get(f'{self.tasks_page_url}/{task_path}')
            num_samples = self.__parse_samples(task_id, task_page)
            click.secho(f'Found {num_samples} samples for task {task_id}.', fg='green', bold=True)

            task = Task(task_id, task_name)
            tasks.append(task)

        return tasks

    def __init__(self, contest_id: str) -> None:
        self.contest_id = contest_id

        scraper = Scraper()

        self.tasks_page_url = f'{Config.WEBSITE_HOST[Website.ATCODER]}/contests/{contest_id}/tasks'
        tasks_page = scraper.get(self.tasks_page_url)

        tasks = self.__parse_tasks(tasks_page)

        super().__init__(tasks)
