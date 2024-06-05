from typing import Optional

from lucy.config import Website
from lucy.filesystem import LocalFS
from lucy.parser_.contest import ContestParser


# pylint: disable=too-many-arguments
def contest_setup(website: Website, contest_id: str, task_id: Optional[str], test_id: Optional[int],
                  n_threads: int, auth: bool) -> None:
    if test_id is not None:
        assert task_id is not None
        raise NotImplementedError()
    contest_ = ContestParser(website, contest_id, task_id, n_threads, auth)
    for task in contest_.parser.tasks:
        LocalFS.store_samples(website, contest_id, task)
        LocalFS.create_impl_file(website, contest_id, task.id_)


# pylint: enable=too-many-arguments
