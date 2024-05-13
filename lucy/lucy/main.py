import os

import click
from click.testing import CliRunner

from lucy import update_snippets as us
from lucy.config import Website
from lucy.parser_.contest import Contest

repo_dir = f'{os.path.dirname(__file__)}/../..'
entry_dir = f'{repo_dir}/common'
snippet_file = f'{repo_dir}/.vscode/cp.code-snippets'


@click.group()
def cli() -> None:
    pass


@cli.command('update-snippets')
@click.option('-ed', '--entry-dir', 'entry_dir_', default=entry_dir, type=click.Path(exists=True))
@click.option('-o', '--out', 'out', default=snippet_file, type=click.Path())
def update_snippets(entry_dir_: str, out: str) -> None:
    entry_dir_ = os.path.abspath(entry_dir)
    out = os.path.abspath(out)
    snippets = us.run(entry_dir_, out)
    click.secho(f'Found {len(snippets)} snippets.', fg='green', bold=True)
    for snippet in snippets:
        click.echo(snippet)


@cli.command('setup')
@click.argument('site', type=click.Choice(['atcoder']))
@click.argument('contest_id')
def setup(site: str, contest_id: str) -> None:
    website = Website.from_string(site)
    print(website)
    contest = Contest(website, contest_id)


if __name__ == '__main__':
    contest = Contest(Website.ATCODER, 'arc177')
