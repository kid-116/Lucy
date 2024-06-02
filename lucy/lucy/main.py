import importlib.metadata
import os
from typing import Any, Optional

import click

from lucy import update_snippets as us, utils
from lucy.config import config, Website
from lucy.filesystem import LocalFS
from lucy.parser_.contest import ContestParser
from lucy.tester import Tester

# pylint: disable=too-many-arguments


@click.group()
@click.version_option(importlib.metadata.version('lucy01'))
@click.pass_context
def lucy(_: Any) -> None:
    """"""  # pylint: disable=empty-docstring
    LocalFS.setup()


@lucy.command('update-snippets')
@click.option('-ed',
              '--entry-dir',
              'entry_dir_',
              default=config.commons.dir_,
              type=click.Path(exists=True),
              help='Root directory for snippet files.')
@click.option('-o',
              '--out',
              'out',
              default=config.snippets.path,
              type=click.Path(),
              help='Output filepath.')
@click.option('-g',
              '--global',
              'global_',
              default=False,
              is_flag=True,
              help='Create a global VSCode snippet file.')
def update_snippets(entry_dir_: str, out: str, global_: bool) -> None:
    """Updates the VSCode snippets file. Generate snippets for all source files in the `entry_dir`.
By default, the `entry_dir` is `$LUCY_HOME/common`. The global snippet file is a link in
`$HOME/.config/Code/User/snippets` to `$LUCY_HOME/.vscode/cp.code-snippets`.
    """
    entry_dir_ = os.path.abspath(entry_dir_)
    out = os.path.abspath(out)
    snippets = us.run(entry_dir_, out)
    click.secho(f'Found {len(snippets)} snippets.', fg='green', bold=True)
    for snippet in snippets:
        click.echo(snippet)
    if global_:
        if not config.snippets.global_link.exists():
            os.symlink(out, config.snippets.global_link)
        else:
            click.secho('Warning: Global snippet file already exists.', fg='yellow', bold=True)


@lucy.command('setup')
@click.argument('site', type=click.Choice(Website.choices()))
@click.argument('contest_id', callback=utils.to_upper)
@click.argument('task_id', required=False, default=None, type=str, callback=utils.to_upper)
@click.argument('test_id', required=False, default=None, type=int)
def setup(site: str, contest_id: str, task_id: Optional[str], test_id: Optional[str]) -> None:
    """Sets up directory structure for a contest.

Example:

    lucy setup AtCoder ABC353
    
It can also be used to fetch a hidden test-case revealed once the contest is completed.

    lucy setup AtCoder ARC177 C in01.txt
    """
    website = Website.from_string(site)
    if test_id is not None:
        assert task_id is not None
        raise NotImplementedError()
    contest_ = ContestParser(website, contest_id, task_id)
    for task in contest_.parser.tasks:
        LocalFS.store_samples(website, contest_id, task)
        LocalFS.create_impl_file(website, contest_id, task.id_)


@lucy.command('test')
@click.argument('site', type=click.Choice(Website.choices()), required=False)
@click.argument('contest_id', type=str, required=False, callback=utils.to_upper)
@click.argument('task_id', type=str, required=False, callback=utils.to_upper)
@click.option('-t',
              '--test-id',
              'test_id',
              default=None,
              type=int,
              help='Select a specific `test_id`')
@click.option('-c',
              '--continue',
              'continue_',
              is_flag=True,
              default=False,
              help='Do not stop on a `WA` verdict.')
@click.option('-v',
              '--verbose',
              'verbose',
              is_flag=True,
              default=False,
              help='Print debug information.')
@click.option('-a',
              '--active',
              'active',
              is_flag=True,
              default=False,
              help='Determine target from current directory.')
def test(site: Optional[str], contest_id: Optional[str], task_id: Optional[str],
         test_id: Optional[int], verbose: bool, continue_: bool, active: bool) -> None:
    """Runs tests for a TASK_ID in a CONTEST_ID for a SITE. If --test-id is not set, all tests are
run.

    lucy test AtCoder ABC353 A 1
    """
    if active:
        site, contest_id, task_id = LocalFS.parse_active_path()
    if any(val is None for val in [site, contest_id, task_id]):
        raise click.ClickException('Could not determine active task.')
    assert site and contest_id and task_id

    website = Website.from_string(site)
    impl_hash = LocalFS.get_impl_hash(website, contest_id, task_id)
    impl_key = utils.hash_((website, contest_id, task_id))
    # print(impl_hash)
    if config.recent_tests.get_cache().get(impl_key) == impl_hash:
        click.secho(config.recent_tests.warning_msg, fg='yellow', bold=True)
    config.recent_tests.get_cache()[impl_key] = impl_hash
    tester = Tester(website, contest_id, task_id, test_id)
    click.secho(f'{website} - {contest_id} - {task_id}', underline=True, bold=True)
    tester.run(verbose, continue_)


@lucy.group('config')
def config_() -> None:
    """Configuration commands."""


@config_.command('get')
@click.argument('key',
                type=click.Choice(list(config.user_cfg.configurables.keys())),
                required=False)
def config_get(key: Optional[str]) -> None:
    """Gets the current configurations. KEY may be used to fetch a specific configuration."""
    for k, val in config.user_cfg.gets().items():
        if key is None or key == k:
            click.echo(f"{k}: {'***' if 'pass' in k.lower() else val}")


@config_.command('setup')
def config_setup() -> None:
    """Sets up the configuration."""
    for key in config.user_cfg.configurables:
        click.echo(f'{key}: ', nl=False)
        val = input()
        if val:
            config.user_cfg.set(key, val)


@config_.command('set')
@click.argument('key', type=click.Choice(list(config.user_cfg.configurables.keys())), required=True)
@click.argument('value', type=str, required=True)
def config_set(key: str, value: str) -> None:
    """Sets value for KEY."""
    config.user_cfg.set(key, value)


@config_.command('unset')
@click.argument('key', type=click.Choice(list(config.user_cfg.configurables.keys())), required=True)
def config_unset(key: str) -> None:
    """Removes KEY configuration value."""
    config.user_cfg.unset(key)
