from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from typing import Generator, Tuple

from lucy import utils
from lucy.browser import Browser
from lucy.config.config import config
from lucy.filesystem import LocalFS
from lucy.types import Contest, Task, Test, Website


class SetupOps:  # pylint: disable=too-few-public-methods

    def __init__(self, n_threads: int, auth: bool):
        self.n_threads = n_threads
        self.auth = auth

    def __parse_tasks(self, contest: Contest) -> list[Task]:
        if contest.site == Website.ATCODER:
            return list(self.__parse_atcoder_tasks(contest))
        raise NotImplementedError()

    def __parse_atcoder_tasks(self, contest: Contest) -> Generator[Task, None, None]:
        browser = Browser()

        tasks_page_url = f'{config.website[contest.site].host}/contests/{contest.contest_id}/tasks'
        browser.driver.get(tasks_page_url)
        tasks_page = browser.get_soup()

        tasks_table = tasks_page.select('table.table tbody tr')
        for row in tasks_table:
            data = row.find_all('td')
            task_id, _ = data[0].text, data[1].text
            yield Task(contest.site, contest.contest_id, task_id)

    def __parse_samples(self, task: Task) -> Tuple[Task, list[Tuple[str, str]]]:
        browser = Browser(authenticate=task.site if self.auth else None)
        if task.site == Website.ATCODER:
            return task, list(self.__parse_atcoder_samples(task, browser))
        raise NotImplementedError()

    def __parse_atcoder_samples(self, task: Task,
                                browser: Browser) -> Generator[Tuple[str, str], None, None]:
        task_url = f'{config.website[task.site].host}/contests/{task.contest_id}/tasks/{task.contest_id}_{task.task_id}'  # pylint: disable=line-too-long
        browser.driver.get(task_url)
        task_page = browser.get_soup()

        for input_, output in utils.batched(task_page.select('pre[id]'), 2):
            yield input_.text, output.text

    def run(self, target: Contest) -> Generator[Tuple[Task, int], None, None]:
        if isinstance(target, Test):
            raise NotImplementedError()
        assert isinstance(target, Contest)

        tasks = [target] if isinstance(target, Task) else self.__parse_tasks(target)

        with ThreadPoolExecutor(max_workers=self.n_threads) as executor:
            threads = [executor.submit(self.__parse_samples, task) for task in tasks]
            for thread in futures.as_completed(threads):
                task, tests = thread.result()
                yield task, len(tests)
                LocalFS.store_samples(task, tests)

        for task in tasks:
            LocalFS.create_impl_file(task)
