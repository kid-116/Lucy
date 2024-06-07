import pytest

from click.testing import CliRunner

from contest_truths import AtCoder
from types_ import ContestTruth

from lucy.main import prune, setup

TESTED_CONTESTS = [
    AtCoder.ABC100,
]


@pytest.fixture(autouse=True)
def setup_contests(runner: CliRunner) -> None:
    for contest in TESTED_CONTESTS:
        runner.invoke(setup, [str(contest.site), contest.contest_id])


@pytest.mark.parametrize('contest', TESTED_CONTESTS)
def test_prune_test(runner: CliRunner, contest: ContestTruth, task_id: str = 'A') -> None:
    task = contest.get_task(task_id)
    orig_num_samples = contest.get_task(task_id).num_samples
    assert task.get_num_tests() == orig_num_samples

    result = runner.invoke(prune, [str(task.site), task.contest_id, task.task_id, str(0)])
    assert result.exit_code == 0
    for test_id in range(orig_num_samples - 1):
        assert task.get_test(test_id).exists()

    result = runner.invoke(
        prune, [str(task.site), task.contest_id, task.task_id,
                str(orig_num_samples - 2)])
    assert result.exit_code == 0
    for test_id in range(orig_num_samples - 2):
        assert task.get_test(test_id).exists()

    result = runner.invoke(prune, [str(task.site), task.contest_id, task.task_id, str(1)])
    assert result.exit_code == 0
    for test_id in range(orig_num_samples - 3):
        assert task.get_test(test_id).exists()


@pytest.mark.parametrize('contest', TESTED_CONTESTS)
def test_prune_task(runner: CliRunner, contest: ContestTruth, task_id: str = 'A') -> None:
    for task in contest.tasks:
        assert task.exists()

    result = runner.invoke(prune, [str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0

    for task in contest.tasks:
        if task.task_id == task_id:
            assert not task.exists()
        else:
            assert task.exists()


@pytest.mark.parametrize('contest', TESTED_CONTESTS)
def test_prune_contest(runner: CliRunner, contest: ContestTruth) -> None:
    assert contest.path.exists()

    result = runner.invoke(prune, [str(contest.site), contest.contest_id])
    assert result.exit_code == 0

    assert not contest.path.exists()
