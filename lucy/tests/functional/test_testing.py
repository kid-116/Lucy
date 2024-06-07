import os
from pathlib import Path
import shutil

from click.testing import CliRunner
import pytest

import conftest
from types_ import ContestTruth

from lucy.config.config import config
from lucy.main import test
from lucy.types import Verdict


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
    task = contest.get_task(task_id)
    shutil.copyfile(
        shared_datadir /
        f'{contest.site.name.lower()}_{contest.contest_id.lower()}_{task_id.lower()}_soln.cpp',
        task.impl_path)
    result = runner.invoke(test, [str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert result.output.count(f'.{Verdict.AC}') == contest.tasks[ord(task_id) -
                                                                  ord('A')].num_samples


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_unchanged_soln_warning(runner: CliRunner,
                                contest: ContestTruth,
                                task_id: str = 'A') -> None:
    config.recent_tests.get_cache().clear()

    result = runner.invoke(test, [str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert config.recent_tests.warning_msg not in result.output

    result = runner.invoke(test, [str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert config.recent_tests.warning_msg in result.output


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_active_flag(runner: CliRunner, contest: ContestTruth, task_id: str = 'A') -> None:
    task_path = contest.get_task(task_id).path

    os.chdir(task_path)
    result = runner.invoke(test, ['-ac'])
    assert result.exit_code == 0

    os.chdir(task_path.parent)
    result = runner.invoke(test, ['-ac'])
    assert result.exit_code != 0
