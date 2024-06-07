import os
from pathlib import Path
import shutil
from typing import Any, Generator, Optional, Tuple

from lucy.config.config import config, Website
from lucy.types import Contest, ContestElement, Task, Test


def batched(iterable: list[Any], n: int) -> Generator[tuple[Any, ...], None, None]:
    l = len(iterable)
    for ndx in range(0, l, n):
        yield tuple(iterable[ndx:min(ndx + n, l)])


def hash_(tuple_: Tuple[Any, ...]) -> str:
    return '-'.join(str(x) for x in tuple_)


def build(site_str: Optional[str] = None,
          contest_id: Optional[str] = None,
          task_id: Optional[str] = None,
          test_id: Optional[int] = None) -> Optional[ContestElement]:
    if not site_str:
        return None
    site = Website.from_string(site_str)
    if not contest_id:
        return site
    if not task_id:
        return Contest(site, contest_id)
    if test_id is None:
        return Task(site, contest_id, task_id)
    return Test(site, contest_id, task_id, test_id)


def get_active_task() -> Task:
    site = None
    contest_id = None
    task_id = None

    active_path = os.path.realpath(os.getcwd())
    home_dir = os.path.realpath(config.home)
    if not active_path.startswith(home_dir):
        raise ValueError('Not in $LUCY_HOME.')

    active_path = active_path[len(home_dir):]
    active_path = active_path.lstrip('/')

    try:
        site, contest_id, task_id = active_path.split('/')[:3]
    except ValueError as e:
        raise ValueError('Not in a task directory.') from e

    return Task(Website.from_string(site), contest_id, task_id)


def init() -> None:
    dir_checks: list[Path] = [
        config.home,
        config.snippets.dir_,
        config.commons.dir_,
        config.storage.path,
        config.storage.acl_path,
    ]

    for dir_ in dir_checks:
        if not dir_.exists():
            print(f'Creating {dir_}')
            os.makedirs(dir_)

    if not os.path.exists(config.commons.template_path):
        print(f'Creating {config.commons.template_path}')
        shutil.copy(config.data_path('template_cpp.cpp'), config.commons.template_path)
