import os
from pathlib import Path
import shutil

from click.testing import CliRunner
import pytest

import conftest
from contest_truths import AtCoder
from types_ import ContestTruth

from lucy.config.config import config
from lucy.filesystem import LocalFS
from lucy.main import test
from lucy.types import Task, Verdict


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_incorrect(runner: CliRunner, contest: ContestTruth, task_id: str = 'A') -> None:
    result = runner.invoke(test, [str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert result.output.count(f'.{Verdict.WA}') == 1

    result = runner.invoke(test, [str(contest.site), contest.contest_id, task_id, '-c'])
    assert result.exit_code == 0
    assert result.output.count(f'.{Verdict.WA}') == contest.tasks[ord(task_id) -
                                                                  ord('A')].num_samples


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_correct(runner: CliRunner,
                 contest: ContestTruth,
                 shared_datadir: Path,
                 task_id: str = 'A') -> None:
    shutil.copyfile(
        shared_datadir /
        f'{contest.site.name.lower()}_{contest.contest_id.lower()}_{task_id.lower()}_soln.cpp',
        LocalFS.get_impl_path(Task.from_contest(contest, task_id)))
    result = runner.invoke(test, [str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert result.output.count(f'.{Verdict.AC}') == contest.tasks[ord(task_id) -
                                                                  ord('A')].num_samples


def test_unchanged_soln_warning(runner: CliRunner,
                                contest: ContestTruth = AtCoder.ABC100,
                                task_id: str = 'A') -> None:
    config.recent_tests.get_cache().clear()

    result = runner.invoke(test, [str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert config.recent_tests.warning_msg not in result.output

    result = runner.invoke(test, [str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert config.recent_tests.warning_msg in result.output


def test_active_flag(runner: CliRunner,
                     contest: ContestTruth = AtCoder.ABC100,
                     task_id: str = 'A') -> None:
    impl_path = LocalFS.get_impl_path(Task.from_contest(contest, task_id), dir_=True)

    os.chdir(impl_path)
    result = runner.invoke(test, ['-ac'])
    assert result.exit_code == 0

    os.chdir(impl_path.parent)
    result = runner.invoke(test, ['-ac'])
    assert result.exit_code != 0
