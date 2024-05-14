import os
import shutil

import click

from lucy import update_snippets as us, utils
from lucy.tester import Tester
from lucy.config import Config, Website
from lucy.parser_.contest import Contest


@click.group()
def cli() -> None:
    pass


@cli.command('update-snippets')
@click.option('-ed',
              '--entry-dir',
              'entry_dir_',
              default=Config.COMMONS_PATH,
              type=click.Path(exists=True))
@click.option('-o', '--out', 'out', default=Config.SNIPPETS_PATH, type=click.Path())
def update_snippets(entry_dir_: str, out: str) -> None:
    entry_dir_ = os.path.abspath(entry_dir_)
    out = os.path.abspath(out)
    snippets = us.run(entry_dir_, out)
    click.secho(f'Found {len(snippets)} snippets.', fg='green', bold=True)
    for snippet in snippets:
        click.echo(snippet)


@cli.command('setup')
@click.argument('site', type=Config.CLI_WEBSITE_CHOICE)
@click.argument('contest_id')
def setup(site: str, contest_id: str) -> None:
    website = Website.from_string(site)
    contest_ = Contest(website, contest_id)
    for task in contest_.parser.tasks:
        impl_path = utils.get_impl_path(website, contest_id, task.id_)
        if not os.path.exists(impl_path):
            shutil.copy(Config.TEMPLATE_PATH, impl_path)


@cli.command('test')
@click.argument('site', type=Config.CLI_WEBSITE_CHOICE)
@click.argument('contest_id')
@click.argument('task_id')
def test(site: str, contest_id: str, task_id: str) -> None:
    website = Website.from_string(site)
    tester = Tester(website, contest_id, task_id)
    tester.run()
