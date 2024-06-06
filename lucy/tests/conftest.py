import os
import shutil
from typing import Generator

from click.testing import CliRunner
import pytest

import contest_truths

from lucy.config.config import config, ConfigClass
from lucy.filesystem import LocalFS
from lucy.main import login, setup
from lucy.types import Website


@pytest.fixture(scope='session')
def runner() -> CliRunner:
    return CliRunner()


TESTED_CONTESTS = [
    contest_truths.AtCoder.ABC100,
]


@pytest.fixture(autouse=True, scope='session')
def setup_env() -> Generator[None, None, None]:
    # Setup.
    LocalFS.setup()

    yield

    # Tear-down.
    shutil.rmtree(config.home)


@pytest.fixture(autouse=True, scope='session')
def setup_contests(runner: CliRunner) -> None:  # pylint: disable=redefined-outer-name
    for contest_truth in TESTED_CONTESTS:
        result = runner.invoke(setup, [str(contest_truth.site), contest_truth.contest_id])
        assert result.exit_code == 0


@pytest.fixture(scope='session', autouse=True)
def login_all(runner: CliRunner) -> None:  # pylint: disable=redefined-outer-name
    for website in Website:
        config.website[website].user_id = os.getenv(f'{str(website).upper()}_USER_ID')
        config.website[website].passwd = os.getenv(f'{str(website).upper()}_PASSWORD')

        result = runner.invoke(login, [str(website)])
        assert result.exit_code == 0
        assert 'Success!' in result.output

        config.website[website].token = ConfigClass().website[website].token
