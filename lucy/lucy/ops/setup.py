from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from typing import Generator, Tuple

from lucy import utils
from lucy.browser import Browser
from lucy.config.config import config
from lucy.filesystem import LocalFS
from lucy.types import Contest, Task, Test, Website


class SetupOps:  # pylint: disable=too-few-public-methods

    @staticmethod
    def __parse_tasks(contest: Contest) -> list[Task]:
        if contest.site == Website.ATCODER:
            return list(SetupOps.__parse_atcoder_tasks(contest))
        raise NotImplementedError()

    @staticmethod
    def __parse_atcoder_tasks(contest: Contest) -> Generator[Task, None, None]:
        browser = Browser()

        tasks_page_url = f'{config.website[contest.site].host}/contests/{contest.contest_id}/tasks'
        browser.driver.get(tasks_page_url)
        tasks_page = browser.get_soup()

        tasks_table = tasks_page.select('table.table tbody tr')
        for row in tasks_table:
            data = row.find_all('td')
            task_id, _ = data[0].text, data[1].text
            yield Task(contest.site, contest.contest_id, task_id)

    @staticmethod
    def __parse_samples(task: Task, auth: bool) -> Tuple[Task, list[Tuple[str, str]]]:
        if task.site == Website.ATCODER:
            return task, list(SetupOps.__parse_atcoder_samples(task, auth))
        raise NotImplementedError()

    @staticmethod
    def __parse_atcoder_samples(task: Task, auth: bool) -> Generator[Tuple[str, str], None, None]:
        browser = Browser(authenticate=task.site if auth else None)
        task_url = f'{config.website[task.site].host}/contests/{task.contest_id}/tasks/{task.contest_id}_{task.task_id}'  # pylint: disable=line-too-long
        browser.driver.get(task_url)
        task_page = browser.get_soup()

        for input_, output in utils.batched(task_page.select('pre[id]'), 2):
            yield input_.text, output.text

    @staticmethod
    def setup(target: Contest | Task | Test, n_threads: int,
              auth: bool) -> Generator[Tuple[Task, int], None, None]:
        if isinstance(target, Test):
            raise NotImplementedError()
        assert isinstance(target, Contest)

        tasks = [target] if isinstance(target, Task) else SetupOps.__parse_tasks(target)

        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            threads = [executor.submit(SetupOps.__parse_samples, task, auth) for task in tasks]
            for thread in futures.as_completed(threads):
                task, tests = thread.result()
                yield task, len(tests)
                LocalFS.store_samples(task, tests)

        for task in tasks:
            LocalFS.create_impl_file(task)
