import os
from pathlib import Path
from subprocess import CalledProcessError

from click.testing import CliRunner
import pytest

import conftest
from types_ import ContestTruth

from lucy.config.config import config
from lucy.main import acl_setup
from lucy.ops.testing import TestingOps

# pylint: disable=protected-access


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_acl(runner: CliRunner,
             shared_datadir: Path,
             contest: ContestTruth,
             task_id: str = 'A') -> None:
    result = runner.invoke(acl_setup, [])
    assert result.exit_code == 0
    assert 'Success!' in result.output

    task = contest.get_task(task_id)
    acl_file = shared_datadir / 'acl.cpp'
    task.impl_path.write_text(acl_file.read_text())

    os.remove(task.path / 'atcoder')

    try:
        TestingOps()._TestingOps__compile(task)  # type: ignore[attr-defined]
        assert False
    except CalledProcessError:
        assert True

    os.symlink(config.storage.acl_path, task.acl_path, target_is_directory=True)
    TestingOps()._TestingOps__compile(task)  # type: ignore[attr-defined]
