import pytest

import utils
from utils import Contest

from lucy.parser_.contest import ContestParser


@pytest.mark.parametrize('contest', [(utils.AtCoder.ABC100)])
def test_parser(contest: Contest) -> None:
    fetched_contest = ContestParser(contest.website, contest.contest_id, n_threads=4)
    fetched_tasks = sorted(fetched_contest.parser.tasks, key=lambda x: x.id_)
    assert len(fetched_contest.parser.tasks) == len(contest.tasks)

    for fetched_task, task in zip(fetched_tasks, contest.tasks):
        assert fetched_task.id_ == task.id_
        assert fetched_task.name == task.name
        assert len(fetched_task.samples) == task.num_samples
