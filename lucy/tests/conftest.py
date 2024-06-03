import shutil
from typing import Any, Generator

from click.testing import CliRunner
import pytest

from lucy.main import config_set
from lucy.config import TestConfig
from lucy.filesystem import LocalFS


@pytest.fixture(scope='session')
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(autouse=True, scope='session')
def setup_env(runner: CliRunner) -> Generator[None, None, None]:  # pylint: disable=redefined-outer-name
    # Setup.
    args: list[Any] = ['NThreads', 1]
    runner.invoke(config_set, args)
    LocalFS.setup()

    yield

    # Tear-down.
    shutil.rmtree(TestConfig.home)
