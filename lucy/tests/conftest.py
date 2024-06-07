import os
import shutil
from typing import Generator

from click.testing import CliRunner
import pytest

import contest_truths

from lucy import utils
from lucy.config.config import config, ConfigClass, Website
from lucy.main import login, setup


@pytest.fixture(scope='session')
def runner() -> CliRunner:
    return CliRunner()


TESTED_CONTESTS = [
    contest_truths.AtCoder.ABC300,
]


@pytest.fixture(autouse=True, scope='session')
def setup_env(runner: CliRunner) -> Generator[None, None, None]:  # pylint: disable=redefined-outer-name
    # Setup.
    utils.init()

    for contest_truth in TESTED_CONTESTS:
        result = runner.invoke(setup, [str(contest_truth.site), contest_truth.contest_id])
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
    shutil.rmtree(config.home)
