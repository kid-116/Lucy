from click.testing import CliRunner
import pytest

import conftest
from types_ import ContestTruth

from lucy.main import submit


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_submit(runner: CliRunner, contest: ContestTruth, task_id: str = 'A') -> None:
    result = runner.invoke(submit, ['-h', str(contest.site), contest.contest_id, task_id])
    assert result.exit_code == 0
