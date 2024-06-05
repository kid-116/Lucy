import os
from typing import Any

from click.testing import CliRunner
import pytest

import conftest
from types_ import ContestTruth

from lucy.filesystem import LocalFS
from lucy.main import setup
from lucy.types import SampleType


@pytest.mark.parametrize('contest_truth', conftest.TESTED_CONTESTS)
def test_setup(runner: CliRunner, contest_truth: ContestTruth) -> None:
    args: list[Any] = [str(contest_truth.site), contest_truth.contest_id]
    result = runner.invoke(setup, args)
    assert result.exit_code == 0

    contest_root_dir = LocalFS.get_contest_root_dir(contest_truth)
    assert os.path.exists(contest_root_dir)

    assert len(os.listdir(contest_root_dir)) == len(contest_truth.tasks)

    for task in contest_truth.tasks:
        task_dir = LocalFS.get_impl_path(task, dir_=True)
        assert os.path.exists(task_dir)

        impl_path = LocalFS.get_impl_path(task)
        assert os.path.exists(impl_path)

        samples_in_dir = LocalFS.get_sample_path(task, type_=SampleType.IN)
        assert os.path.exists(samples_in_dir)
        assert len(os.listdir(samples_in_dir)) == task.num_samples

        samples_out_dir = LocalFS.get_sample_path(task, type_=SampleType.OUT)
        assert os.path.exists(samples_out_dir)
        assert len(os.listdir(samples_out_dir)) == task.num_samples
