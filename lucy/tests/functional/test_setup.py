import os

from click.testing import CliRunner
import pytest

import utils
from utils import Contest

from lucy.config import SampleType
from lucy.filesystem import LocalFS
from lucy.main import setup


@pytest.mark.parametrize('contest', [(utils.AtCoder.ABC100)])
def test_setup(runner: CliRunner, contest: Contest) -> None:
    result = runner.invoke(setup, [str(contest.website), contest.contest_id])
    assert result.exit_code == 0

    contest_root_dir = LocalFS.get_contest_root_dir(contest.website, contest.contest_id)
    assert os.path.exists(contest_root_dir)

    assert len(os.listdir(contest_root_dir)) == len(contest.tasks)

    for task in contest.tasks:
        task_dir = LocalFS.get_impl_path(contest.website, contest.contest_id, task.id_, dir_=True)
        assert os.path.exists(task_dir)

        impl_path = LocalFS.get_impl_path(contest.website, contest.contest_id, task.id_)
        assert os.path.exists(impl_path)

        samples_in_dir = LocalFS.get_sample_path(contest.website,
                                                 contest.contest_id,
                                                 task.id_,
                                                 type_=SampleType.IN)
        assert os.path.exists(samples_in_dir)
        assert len(os.listdir(samples_in_dir)) == task.num_samples

        samples_out_dir = LocalFS.get_sample_path(contest.website,
                                                  contest.contest_id,
                                                  task.id_,
                                                  type_=SampleType.OUT)
        assert os.path.exists(samples_out_dir)
        assert len(os.listdir(samples_out_dir)) == task.num_samples
