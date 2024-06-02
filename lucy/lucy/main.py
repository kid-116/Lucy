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
        os.symlink(out,
                   f'{os.getenv("HOME")}/.config/Code/User/snippets/{config.snippets.file_name}')


@lucy.command('setup')
@click.argument('site', type=click.Choice(Website.choices()))
@click.argument('contest_id')
@click.argument('task_id', required=False, default=None, type=str)
@click.argument('test_id', required=False, default=None, type=str)
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
@click.argument('site', type=click.Choice(Website.choices()), required=True)
@click.argument('contest_id', type=str, required=True)
@click.argument('task_id', type=str, required=True)
@click.argument('test_id', default=None, type=int, required=False)
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
def test(site: str, contest_id: str, task_id: str, test_id: Optional[int], verbose: bool,
         continue_: bool) -> None:
    """Run tests for a TASK_ID in a CONTEST_ID for a SITE. If TEST_ID is not provided, all tests are
run.

    lucy test AtCoder ABC353 A 1
    """
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


@lucy.command('active-test')
@click.argument('test_id', default=None, type=int, required=False)
@click.option('-v',
              '--verbose',
              'verbose',
              is_flag=True,
              default=False,
              help='Print debug information.')
@click.option('-c',
              '--continue',
              'continue_',
              is_flag=True,
              default=False,
              help='Do not stop on a `WA` verdict.')
@click.pass_context
def active_test(ctx: Any, test_id: Optional[int], verbose: bool, continue_: bool) -> None:
    """Run tests by determining the task using the current working directory.

    AtCoder/ABC353/A$ lucy active-test
    """
    site, contest_id, task_id = LocalFS.parse_active_path()
    if not site:
        click.secho('Could not determine `site`.', fg='red', bold=True, err=True)
        return
    if not contest_id:
        click.secho('Could not determine `contest_id`.', fg='red', bold=True, err=True)
        return
    if not task_id:
        click.secho('Could not determine `task_id`.', fg='red', bold=True, err=True)
        return

    ctx.invoke(test,
               site=str(Website.from_string(site)),
               contest_id=contest_id,
               task_id=task_id,
               test_id=test_id,
               verbose=verbose,
               continue_=continue_)
