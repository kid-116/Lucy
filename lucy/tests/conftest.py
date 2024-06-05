import os
import shutil
from typing import Generator

from click.testing import CliRunner
import pytest

import utils

from lucy.config import config, ConfigClass, TestConfig, Website
from lucy.filesystem import LocalFS
from lucy.main import setup, login


@pytest.fixture(scope='session')
def runner() -> CliRunner:
    return CliRunner()


TESTED_CONTESTS = [
    utils.AtCoder.ABC100,
]


@pytest.fixture(autouse=True, scope='session')
def setup_env(runner: CliRunner) -> Generator[None, None, None]:  # pylint: disable=redefined-outer-name
    # Setup.
    LocalFS.setup()

    for contest in TESTED_CONTESTS:
        result = runner.invoke(setup, [str(contest.website), contest.contest_id])
        assert result.exit_code == 0

    for website in Website:
        config.website[website].user_id = os.getenv(f'{str(website).upper()}_USER_ID')
        config.website[website].passwd = os.getenv(f'{str(website).upper()}_PASSWORD')

        result = runner.invoke(login, [str(website)])
        assert result.exit_code == 0
        assert 'Success!' in result.output

        config.website[website].token = ConfigClass().website[website].token

    yield

    # Tear-down.
    shutil.rmtree(TestConfig.home)
