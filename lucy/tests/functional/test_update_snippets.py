from click.testing import CliRunner

from lucy.main import update_snippets


def test_update_snippets(runner: CliRunner) -> None:
    result = runner.invoke(update_snippets, [])
    assert result.exit_code == 0
