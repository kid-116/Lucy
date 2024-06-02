import shutil
from typing import Generator

from click.testing import CliRunner
import pytest

from lucy.config import Config
from lucy.filesystem import LocalFS


@pytest.fixture(autouse=True, scope='session')
def setup_env() -> Generator[None, None, None]:
    # Setup.
    lucy_home = '/tmp/lucy'
    Config.LUCY_HOME = lucy_home
    LocalFS.setup()

    yield

    # Tear-down.
    shutil.rmtree(lucy_home)


@pytest.fixture(scope='session')
def runner() -> CliRunner:
    return CliRunner()
