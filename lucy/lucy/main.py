import importlib.metadata
import os
from typing import Any, Optional

import click

from lucy import update_snippets as us
from lucy.config import Config, SampleType, Website
from lucy.dbx_client import DropboxClient
from lucy.filesystem import LocalFS
from lucy.parser_.contest import ContestParser
from lucy.tester import Tester

# pylint: disable=too-many-arguments


@click.group()
@click.version_option(importlib.metadata.version('lucy01'))
@click.pass_context
def cli(_: Any) -> None:
    LocalFS.setup()


@cli.command('update-snippets')
@click.option('-ed',
              '--entry-dir',
              'entry_dir_',
              default=Config.COMMONS_DIR,
              type=click.Path(exists=True))
@click.option('-o', '--out', 'out', default=Config.SNIPPETS_PATH, type=click.Path())
@click.option('-g', '--global', 'global_', default=False, is_flag=True)
def update_snippets(entry_dir_: str, out: str, global_: bool) -> None:
    entry_dir_ = os.path.abspath(entry_dir_)
    out = os.path.abspath(out)
    snippets = us.run(entry_dir_, out)
    click.secho(f'Found {len(snippets)} snippets.', fg='green', bold=True)
    for snippet in snippets:
        click.echo(snippet)
    if global_:
        os.symlink(out,
                   f'{os.getenv("HOME")}/.config/Code/User/snippets/{Config.SNIPPETS_FILE_NAME}')


@cli.command('setup')
@click.argument('site', type=Config.CLI_WEBSITE_CHOICE)
@click.argument('contest_id')
@click.argument('task_id', required=False, default=None, type=str)
@click.argument('test_id', required=False, default=None, type=str)
def setup(site: str, contest_id: str, task_id: Optional[str], test_id: Optional[str]) -> None:
    website = Website.from_string(site)
    if test_id is not None:
        assert task_id is not None
        if website != Website.ATCODER:
            raise NotImplementedError()
        in_path, out_path, idx = LocalFS.get_new_sample_paths(website, contest_id, task_id)
        DropboxClient().download(f'/{contest_id}/{task_id}/{SampleType.IN}/{test_id}', in_path)
        DropboxClient().download(f'/{contest_id}/{task_id}/{SampleType.OUT}/{test_id}', out_path)
        click.secho(f'Stored sample {test_id} as Test#{idx:02d}.', fg='green', bold=True)
        return
    contest_ = ContestParser(website, contest_id, task_id)
    for task in contest_.parser.tasks:
        LocalFS.store_samples(website, contest_id, task)
        LocalFS.create_impl_file(website, contest_id, task.id_)


@cli.command('test')
@click.argument('site', type=Config.CLI_WEBSITE_CHOICE, required=True)
@click.argument('contest_id', type=str, required=True)
@click.argument('task_id', type=str, required=True)
@click.argument('test_id', default=None, type=int, required=False)
@click.option('-c', '--continue', 'continue_', is_flag=True, default=False)
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
def test(site: str, contest_id: str, task_id: str, test_id: Optional[int], verbose: bool,
         continue_: bool) -> None:
    website = Website.from_string(site)
    tester = Tester(website, contest_id, task_id, test_id)
    click.secho(f'{website} - {contest_id} - {task_id}', underline=True, bold=True)
    tester.run(verbose, continue_)


@cli.command('active-test')
@click.argument('test_id', default=None, type=int, required=False)
@click.option('-v', '--verbose', 'verbose', is_flag=True, default=False)
@click.option('-c', '--continue', 'continue_', is_flag=True, default=False)
@click.pass_context
def active_test(ctx: Any, test_id: Optional[int], verbose: bool, continue_: bool) -> None:
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
               site=site,
               contest_id=contest_id,
               task_id=task_id,
               test_id=test_id,
               verbose=verbose,
               continue_=continue_)
