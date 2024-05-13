import os
import shutil
import subprocess

import click

from lucy import update_snippets as us
from lucy.config import Config, SampleType, Website
from lucy.parser_.contest import Contest


@click.group()
def cli() -> None:
    if not os.path.exists(Config.LUCY_HOME):
        os.makedirs(Config.LUCY_HOME)
    if not os.path.exists(Config.LUCY_STORAGE):
        os.makedirs(Config.LUCY_STORAGE)


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
@click.option('-f', '--force', 'force', type=bool, is_flag=True, default=False)
def setup(site: str, contest_id: str, force: bool) -> None:
    website = Website.from_string(site)
    samples_root = Config.get_samples_root(website, contest_id)
    if os.path.exists(samples_root):
        if not force:
            click.secho('Setup already completed! Try running with the flag `-f`.')
        else:
            click.echo('Removing existing samples ...')
            shutil.rmtree(samples_root)
    contest_ = Contest(website, contest_id)
    click.echo('Creating implementation directories ...')
    for task in contest_.parser.tasks:
        task_dir = f'{Config.get_implementation_root(website, contest_id, task.id_)}'
        os.makedirs(task_dir, exist_ok=True)
        shutil.copy(Config.TEMPLATE_PATH,
                    Config.get_implementation_path(website, contest_id, task.id_))


@cli.command('test')
@click.argument('site', type=Config.CLI_WEBSITE_CHOICE)
@click.argument('contest_id')
@click.argument('task_id')
def test(site: str, contest_id: str, task_id: str) -> None:
    website = Website.from_string(site)
    samples_root = Config.get_samples_root(website, contest_id, task_id, SampleType.IN)
    impl_path = Config.get_implementation_path(website, contest_id, task_id)
    bin_path = f'{os.path.dirname(impl_path)}/{Config.COMPLILED_FILE_NAME}'
    subprocess.check_call(['g++', impl_path, '-o', bin_path])
    for idx, file in enumerate(os.listdir(samples_root)):
        click.echo(file, nl=False)
        process = subprocess.Popen([bin_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        if process.stdin:
            with open(f'{samples_root}/{file}') as f:
                process.stdin.write(f.read().encode())
            process.stdin.close()
        if not process.stdout:
            raise Exception()
        output = process.stdout.read().decode()
        truth_out_path = Config.get_sample_path(website, contest_id, task_id, SampleType.OUT, idx)
        with open(truth_out_path) as f:
            truth = f.read()
            click.echo(f'{"." * 50}', nl=False)
            if output.strip() == truth.strip():
                click.secho('AC', bg='green')
            else:
                click.secho('WA', bg='red')
                click.echo('Expected:\n' + truth)
                click.echo('Got:\n' + output)
        process.wait()


if __name__ == '__main__':
    contest = Contest(Website.ATCODER, 'arc177')
