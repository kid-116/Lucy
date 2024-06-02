from pathlib import Path
import shutil

from click.testing import CliRunner
import pytest

import utils
from utils import Contest

from lucy.config import config
from lucy.filesystem import LocalFS
from lucy.main import test

from . import test_setup

TESTED_CONTESTS = [
    utils.AtCoder.ABC100,
]


@pytest.fixture(autouse=True, scope='session')
def setup(runner: CliRunner) -> None:
    for contest in TESTED_CONTESTS:
        test_setup.test_setup(runner, contest)


@pytest.mark.parametrize('contest', TESTED_CONTESTS)
def test_incorrect(runner: CliRunner, contest: Contest, task_id: str = 'A') -> None:
    result = runner.invoke(test, [str(contest.website), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert result.output.count('.WA') == 1

    result = runner.invoke(test, [str(contest.website), contest.contest_id, task_id, '-c'])
    assert result.exit_code == 0
    assert result.output.count('.WA') == contest.tasks[ord(task_id) - ord('A')].num_samples


@pytest.mark.parametrize('contest', TESTED_CONTESTS)
def test_correct(runner: CliRunner, contest: Contest, datadir: Path, task_id: str = 'A') -> None:
    shutil.copyfile(
        datadir /
        f'{contest.website.name.lower()}_{contest.contest_id.lower()}_{task_id.lower()}_soln.cpp',
        LocalFS.get_impl_path(contest.website, contest.contest_id, task_id))
    result = runner.invoke(test, [str(contest.website), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert result.output.count('.AC') == contest.tasks[ord(task_id) - ord('A')].num_samples


def test_unchanged_soln_warning(runner: CliRunner,
                                contest: Contest = utils.AtCoder.ABC100,
                                task_id: str = 'A') -> None:
    config.recent_tests.get_cache().clear()

    result = runner.invoke(test, [str(contest.website), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert config.recent_tests.warning_msg not in result.output

    result = runner.invoke(test, [str(contest.website), contest.contest_id, task_id])
    assert result.exit_code == 0
    assert config.recent_tests.warning_msg in result.output
