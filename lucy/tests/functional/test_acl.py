import os
from pathlib import Path
from subprocess import CalledProcessError

from click.testing import CliRunner

from lucy.config.config import config, Website
from lucy.main import acl_setup
from lucy.ops.testing import TestingOps
from lucy.types import Task

def test_acl(runner: CliRunner, shared_datadir: Path) -> None:
    result = runner.invoke(acl_setup, [])
    assert result.exit_code == 0
    assert 'Success!' in result.output

    task = Task(Website.ATCODER, 'ABC100', 'A')
    acl_file = shared_datadir / 'acl.cpp'
    task.impl_path.write_text(acl_file.read_text())

    os.remove(task.path / 'atcoder')

    try:
        TestingOps()._TestingOps__compile(task)
        assert False
    except CalledProcessError:
        assert True

    os.symlink(config.storage.acl_path, task.acl_path, target_is_directory=True)
    TestingOps()._TestingOps__compile(task)
