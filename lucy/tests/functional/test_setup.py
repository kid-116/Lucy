import os
from typing import Any

from click.testing import CliRunner
import pytest

import conftest
from contest_truths import AtCoder
from types_ import ContestTruth

from lucy.filesystem import LocalFS
from lucy.main import setup
from lucy.types import SampleType, Task, Test


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_setup(runner: CliRunner, contest: ContestTruth) -> None:
    args: list[Any] = [str(contest.site), contest.contest_id]
    result = runner.invoke(setup, args)
    assert result.exit_code == 0

    contest_root_dir = LocalFS.get_contest_root_dir(contest)
    assert os.path.exists(contest_root_dir)

    assert len(os.listdir(contest_root_dir)) == len(contest.tasks)

    for task in contest.tasks:
        task_dir = LocalFS.get_impl_path(task, dir_=True)
        assert os.path.exists(task_dir)

        impl_path = LocalFS.get_impl_path(task)
        assert os.path.exists(impl_path)

        samples_in_dir = LocalFS.get_sample_path(task, type_=SampleType.IN)
        assert os.path.exists(samples_in_dir)
        assert len(os.listdir(samples_in_dir)) == task.num_samples

        samples_out_dir = LocalFS.get_sample_path(task, type_=SampleType.OUT)
        assert os.path.exists(samples_out_dir)
        assert len(os.listdir(samples_out_dir)) == task.num_samples


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_setup_single(runner: CliRunner, contest: ContestTruth, task_id: str = 'A') -> None:
    result = runner.invoke(setup, [str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert result.output.count('Found') == 1


@pytest.mark.parametrize('contest,task_id,test_id', [(AtCoder.ABC100, 'A', 'in01.txt')])
def test_setup_hidden(runner: CliRunner, contest: ContestTruth, task_id: str, test_id: str) -> None:
    result = runner.invoke(setup, [str(contest.site), contest.contest_id, task_id, test_id])
    assert result.exit_code == 0
    task = Task.from_contest(contest, task_id)
    assert LocalFS.num_samples(task) == 7
    test = Test.from_task(task, 6)
    LocalFS.delete(LocalFS.get_sample_path(test, type_=SampleType.IN))
    LocalFS.delete(LocalFS.get_sample_path(test, type_=SampleType.OUT))
