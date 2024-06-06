import importlib.metadata
import time
from typing import Any, Optional

import click

from lucy import utils
from lucy.auth import Auth
from lucy.config.config import config
from lucy.filesystem import LocalFS
from lucy.ops.setup import SetupOps
from lucy.ops.snippets import SnippetOps
from lucy.ops.submit import SubmitOps
from lucy.ops.testing import TestingOps
from lucy.params.args import Arguments
from lucy.params.opts import Options
from lucy.types import Contest, Task, Test, Verdict, Website

# pylint: disable=too-many-arguments


@click.group()
@click.version_option(importlib.metadata.version('lucy01'))
@click.pass_context
def lucy(_: Any) -> None:
    """"""  # pylint: disable=empty-docstring
    LocalFS.setup()


@lucy.command('update-snippets')
@Options.global_(help_='Create a global VSCode snippet file.')
@Options.force(help_='Force update.')
def update_snippets(global_: bool, force: bool) -> None:
    """Updates the VSCode snippets file. Generate snippets for all source files in the `entry_dir`.
By default, the `entry_dir` is `$LUCY_HOME/common`. The global snippet file is a link in
`$HOME/.config/Code/User/snippets` to `$LUCY_HOME/.vscode/cp.code-snippets`.
    """
    snippets = list(SnippetOps().update())
    click.secho(f'Found {len(snippets)} snippets.', fg='green', bold=True)
    for snippet in snippets:
        click.echo(snippet)
    if global_:
        already_present = LocalFS.create_global_snippets_link(force)
        if already_present:
            click.secho('Warning: Global snippet file already exists.', fg='yellow', bold=True)


@lucy.command('setup')
@Arguments.site(required=True)
@Arguments.contest_id(required=True)
@Arguments.task_id(required=False)
@Arguments.test_id(required=False)
@Options.n_threads()
@Options.authenticate()
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
    target = utils.build(site, contest_id, task_id, test_id)
    assert isinstance(target, Contest)
    for task, num_samples in SetupOps(n_threads, auth).run(target):
        click.secho(f'Found {num_samples} samples for task {task.task_id}.', fg='green', bold=True)
    end = time.time()
    click.secho(f'Finished in {end - start} sec(s).')


@lucy.command('test')
@Arguments.site(required=False)
@Arguments.contest_id(required=False)
@Arguments.task_id(required=False)
@Options.test_id()
@Options.continue_('Do not stop on a `WA` verdict.')
@Options.active()
@Options.verbose()
def test(site: Optional[str], contest_id: Optional[str], task_id: Optional[str],
         test_id: Optional[int], verbose: bool, continue_: bool, active: bool) -> None:
    """Runs tests for a TASK_ID in a CONTEST_ID for a SITE. If --test-id is not set, all tests are
run.

    lucy test AtCoder ABC353 A 1
    """
    target = utils.build(site, contest_id, task_id, test_id)
    if active:
        task = LocalFS.parse_active_path()
        if test_id:
            target = Test.from_task(task, test_id)
        else:
            target = task
    assert isinstance(target, Task)

    impl_hash = LocalFS.get_impl_hash(target)
    impl_key = utils.hash_((target.site, target.contest_id, target.task_id))
    if config.recent_tests.get_cache().get(impl_key) == impl_hash:
        click.secho(config.recent_tests.warning_msg, fg='yellow', bold=True)
    config.recent_tests.get_cache()[impl_key] = impl_hash
    click.secho(str(target), underline=True, bold=True)
    results = TestingOps(verbose, continue_).run(target)
    for idx, result in enumerate(results):
        if result is None:
            continue
        click.echo(f'Test#{idx:02d}/{len(results) - 1:02d}', nl=False)
        click.echo(f'{"." * 50}', nl=False)
        verdict: Verdict = Verdict.WA if isinstance(result, str) else Verdict.AC
        verdict.echo()
        if isinstance(result, str) and verbose:
            test = Test.from_task(target, idx)
            in_txt, truth_txt = LocalFS.load_test(test)
            click.secho("Input:", bg='white', bold=True)
            print(in_txt.strip())
            click.secho("Output:", bg='red', bold=True)
            print(result.strip())
            click.secho("Expected:", bg='green', bold=True)
            print(truth_txt.strip())

@lucy.command('submit')
@Arguments.site(required=False)
@Arguments.contest_id(required=False)
@Arguments.task_id(required=False)
@Options.active()
@Options.hidden(help_='Do not show submission in browser.')
def submit(site: Optional[str], contest_id: Optional[str], task_id: Optional[str], active: bool,
           hidden: bool) -> None:
    """Submits solution for TASK_ID in a CONTEST_ID to a SITE.

    lucy submit AtCoder ABC353 A
    """
    target = utils.build(site, contest_id, task_id)
    if active:
        target = LocalFS.parse_active_path()
    assert isinstance(target, Task)

    SubmitOps().submit(target, hidden)


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
    Auth.login(Website.from_string(site))
    click.secho('Success!', fg='green', bold=True)
