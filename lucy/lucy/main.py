import importlib.metadata
import os
import time
from typing import Any, Optional

import click

from lucy import contest_setup
from lucy import update_snippets as us, utils
from lucy.auth import Auth
from lucy.config import config, Website
from lucy.filesystem import LocalFS
from lucy import submit_task
from lucy.tester import Tester
from lucy.utils import Arguments, Options

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
@Options.force(help_='Force update.')
def update_snippets(entry_dir_: str, out: str, global_: bool, force: bool) -> None:
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
        link_absent = not config.snippets.global_link.exists()
        if link_absent or force:
            if not link_absent:
                os.remove(config.snippets.global_link)
            os.symlink(out, config.snippets.global_link)
        else:
            click.secho('Warning: Global snippet file already exists.', fg='yellow', bold=True)


@lucy.command('setup')
@Arguments.site(required=True)
@Arguments.contest_id(required=True)
@Arguments.task_id(required=False)
@Arguments.test_id(required=False)
@click.option('-t',
              '--n-threads',
              'n_threads',
              default=config.n_threads,
              type=int,
              help='Number of execution threads. Warning: Can be flaky!')
@click.option('-a', '--auth', 'auth', is_flag=True, default=False, help='Authenticate.')
def setup(site: str, contest_id: str, task_id: Optional[str], test_id: Optional[int],
          n_threads: int, auth: bool) -> None:
    """Sets up directory structure for a contest.

Example:

    lucy setup AtCoder ABC353
    
It can also be used to fetch a hidden test-case revealed once the contest is completed.

    lucy setup AtCoder ARC177 C in01.txt
    """
    click.echo(f'Using {n_threads} thread(s).')
    start = time.time()
    website = Website.from_string(site)
    contest_setup.contest_setup(website, contest_id, task_id, test_id, n_threads, auth)
    end = time.time()
    click.secho(f'Finished in {end - start} sec(s).')


@lucy.command('test')
@Arguments.site(required=False)
@Arguments.contest_id(required=False)
@Arguments.task_id(required=False)
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
@Options.verbose()
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
    if config.recent_tests.get_cache().get(impl_key) == impl_hash:
        click.secho(config.recent_tests.warning_msg, fg='yellow', bold=True)
    config.recent_tests.get_cache()[impl_key] = impl_hash
    tester = Tester(website, contest_id, task_id, test_id)
    click.secho(f'{website} - {contest_id} - {task_id}', underline=True, bold=True)
    tester.run(verbose, continue_)


@lucy.command('submit')
@Arguments.site(required=False)
@Arguments.contest_id(required=False)
@Arguments.task_id(required=False)
@click.option('-a',
              '--active',
              'active',
              is_flag=True,
              default=False,
              help='Determine target from current directory.')
@click.option('-h',
              '--hidden',
              'hidden',
              is_flag=True,
              default=False,
              help='Do not show submission in browser.')
def submit(site: Optional[str], contest_id: Optional[str], task_id: Optional[str], active: bool,
           hidden: bool) -> None:
    """Submits solution for TASK_ID in a CONTEST_ID to a SITE.

    lucy test AtCoder ABC353 A 1
    """
    if active:
        site, contest_id, task_id = LocalFS.parse_active_path()
    if any(val is None for val in [site, contest_id, task_id]):
        raise click.ClickException('Could not determine active task.')
    assert site and contest_id and task_id
    website = Website.from_string(site)
    submit_task.submit(website, contest_id, task_id, hidden)


@lucy.group('config')
def config_() -> None:
    """Configuration commands."""


@config_.command('get')
@Arguments.config_key(required=False)
def config_get(key: Optional[str]) -> None:
    """Gets the current configurations. KEY may be used to fetch a specific configuration."""
    for k, val in config.user_cfg.gets().items():
        if key is None or key == k:
            is_secret = any(
                keyword in k.lower() for keyword in ['pass', 'token']) and val is not None
            click.echo(f"{k}: {'***' if is_secret else val}")


@config_.command('setup')
def config_setup() -> None:
    """Sets up the configuration."""
    for key in config.user_cfg.configurables:
        click.echo(f'{key}: ', nl=False)
        val = input()
        if val:
            config.user_cfg.set(key, val)


@config_.command('set')
@Arguments.config_key(required=True)
@Arguments.config_value(required=True)
def config_set(key: str, value: str) -> None:
    """Sets value for KEY."""
    config.user_cfg.set(key, value)


@config_.command('unset')
@Arguments.config_key(required=True)
def config_unset(key: str) -> None:
    """Removes KEY configuration value."""
    config.user_cfg.unset(key)


@lucy.command('login')
@Arguments.site(required=True)
def login(site: str) -> None:
    """Authenticates for SITE. It is necessary when a accessing contest tasks requires signing in.
For example, AtCoder requires signing in to access **ongoing** contest tasks. To login successfully,
you must have the required credentials set in the configuration.
    """
    website = Website.from_string(site)
    Auth.login(website)
    click.secho('Success!', fg='green', bold=True)
