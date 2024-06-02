import tempfile

from click.testing import CliRunner

from lucy.main import update_snippets


def test_update_snippets(runner: CliRunner) -> None:
    with tempfile.NamedTemporaryFile() as snippets_file_tmp:
        result = runner.invoke(update_snippets, ['-o', snippets_file_tmp.name])
        assert result.exit_code == 0
