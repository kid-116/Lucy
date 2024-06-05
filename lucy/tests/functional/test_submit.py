from click.testing import CliRunner
import pytest

import conftest
from utils import Contest

from lucy.main import submit


@pytest.mark.parametrize('contest', conftest.TESTED_CONTESTS)
def test_submit(runner: CliRunner, contest: Contest, task_id: str = 'A') -> None:
    result = runner.invoke(submit, [str(contest.website), contest.contest_id, task_id])
    assert result.exit_code == 0
