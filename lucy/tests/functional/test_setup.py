import os
from typing import Any

from click.testing import CliRunner
import pytest

import conftest
from contest_truths import AtCoder
from types_ import ContestTruth

from lucy.main import setup

# pylint: disable=too-many-arguments


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_setup(runner: CliRunner, contest: ContestTruth) -> None:
    result = runner.invoke(setup, [str(contest.site), contest.contest_id])
    assert result.exit_code == 0
    skipped_tasks = [task.task_id for task in contest.tasks]
    assert f"Skipping existing task(s) - {', '.join(skipped_tasks)}." in result.output


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_setup_force(runner: CliRunner, contest: ContestTruth) -> None:
    args: list[Any] = ['-f', str(contest.site), contest.contest_id]
    result = runner.invoke(setup, args)
    assert result.exit_code == 0

    assert os.path.exists(contest.path)
    assert len(os.listdir(contest.path)) == len(contest.tasks)

    for task in contest.tasks:
        assert task.path.exists()
        assert task.impl_path.exists()
        assert task.test_in_dir.exists()
        assert task.acl_path.exists()
        assert len(os.listdir(task.test_in_dir)) == task.num_samples

        assert task.test_out_dir.exists()
        assert len(os.listdir(task.test_out_dir)) == task.num_samples


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_setup_single(runner: CliRunner, contest: ContestTruth, task_id: str = 'A') -> None:
    result = runner.invoke(setup, ['-f', str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert result.output.count('Found') == 2


@pytest.mark.parametrize('contest,task_id,test_id,in_txt,out_txt',
                         [(AtCoder.ABC100, 'A', 'in01.txt', '1 1', 'Yay!')])
def test_setup_hidden(runner: CliRunner, contest: ContestTruth, task_id: str, test_id: str,
                      in_txt: str, out_txt: str) -> None:
    result = runner.invoke(setup, [str(contest.site), contest.contest_id, task_id, test_id])
    assert result.exit_code == 0
    task = contest.get_task(task_id)
    assert task.get_num_tests() == 7
    test = task.get_test(6)
    assert (in_txt, out_txt) == test.load()
    test.delete()
