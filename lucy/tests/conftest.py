import os
import shutil
from typing import Generator

from click.testing import CliRunner
import pytest

from lucy.config import TestConfig
from lucy.filesystem import LocalFS


@pytest.fixture(autouse=True, scope='session')
def setup_env() -> Generator[None, None, None]:
    # Setup.
    LocalFS.setup()

    yield

    # Tear-down.
    shutil.rmtree(TestConfig.home)


@pytest.fixture(scope='session')
def runner() -> CliRunner:
    return CliRunner()
