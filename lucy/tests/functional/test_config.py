from click.testing import CliRunner

from lucy.config.config import config, ConfigClass
from lucy.main import config_get, config_set, config_unset
from lucy.types import Website


def test_config_get(runner: CliRunner) -> None:
    result = runner.invoke(config_get, [])
    assert result.exit_code == 0
    for key in config.user_cfg.configurables:
        assert f'{key}: ' in result.output
    assert result.output.count('\n') == len(config.user_cfg.configurables)


def test_config_get_single(runner: CliRunner, key: str = 'AtCoder.UserId') -> None:
    result = runner.invoke(config_get, [key])
    assert result.exit_code == 0
    assert result.output.count('\n') == 1
    assert f'{key}: ' in result.output


def test_config_set_str(runner: CliRunner) -> None:
    key = 'AtCoder.UserId'
    val = 'kid116'

    result = runner.invoke(config_set, [key, val])
    assert result.exit_code == 0

    result = runner.invoke(config_get, [key])
    assert result.exit_code == 0
    assert result.output.count('\n') == 1
    assert f'{key}: {val}' in result.output

    assert ConfigClass().website[Website.ATCODER].user_id == val
    assert isinstance(ConfigClass().website[Website.ATCODER].user_id, str)


def test_config_set_int(runner: CliRunner) -> None:
    key = 'NThreads'
    val = 1

    result = runner.invoke(config_set, [key, str(val)])
    assert result.exit_code == 0

    result = runner.invoke(config_get, [key])
    assert result.exit_code == 0
    assert result.output.count('\n') == 1
    assert f'{key}: {val}' in result.output

    assert ConfigClass().n_threads == val
    assert isinstance(ConfigClass().n_threads, int)


def test_config_unset(runner: CliRunner) -> None:
    key = 'AtCoder.UserId'

    result = runner.invoke(config_unset, [key])
    assert result.exit_code == 0

    result = runner.invoke(config_get, [key])
    assert result.exit_code == 0
    assert result.output.count('\n') == 1
    assert f'{key}: None' in result.output

    assert ConfigClass().website[Website.ATCODER].user_id is None
