import os
import shutil
from typing import Generator, Optional, Tuple

import click

from lucy.config import Config, SampleType, Website
from lucy.parser_.parser_ import Task


class LocalFS:

    @staticmethod
    def get_impl_path(website: Website,
                      contest_id: str,
                      task_id: str,
                      dir_: bool = False,
                      bin_: bool = False) -> str:
        impl_path = f'{Config.LUCY_HOME}/{website}/{contest_id.upper()}/{task_id.upper()}'
        if bin_:
            return f'{impl_path}/{Config.IMPL_BIN}'
        if not dir_:
            impl_path = f'{impl_path}/{Config.IMPL_MAIN}'
        return impl_path

    @staticmethod
    def get_sample_path(website: Website,
                        contest_id: str,
                        task_id: str,
                        type_: Optional[SampleType] = None,
                        idx: Optional[int] = None) -> str:
        sample_path = LocalFS.get_impl_path(website, contest_id, task_id, dir_=True)
        sample_path += f'/{Config.SAMPLES_DIR}'
        if type_:
            sample_path += f'/{type_}'
            if idx is not None:
                sample_path += f'/{idx:02d}.txt'
        return sample_path

    @staticmethod
    def delete_samples(website: Website, contest_id: str, task_id: str) -> bool:
        samples_dir = LocalFS.get_sample_path(website, contest_id, task_id)
        if os.path.exists(samples_dir):
            shutil.rmtree(samples_dir)
            return False
        return True

    @staticmethod
    def num_samples(website: Website, contest_id: str, task_id: str) -> int:
        return len(os.listdir(LocalFS.get_sample_path(website, contest_id, task_id, SampleType.IN)))

    @staticmethod
    def get_new_sample_paths(website: Website, contest_id: str,
                             task_id: str) -> Tuple[str, str, int]:
        idx = LocalFS.num_samples(website, contest_id, task_id)
        in_path = LocalFS.get_sample_path(website, contest_id, task_id, SampleType.IN, idx)
        out_path = LocalFS.get_sample_path(website, contest_id, task_id, SampleType.OUT, idx)
        return in_path, out_path, idx

    @staticmethod
    def store_sample(website: Website, contest_id: str, task_id: str, sample: Tuple[str,
                                                                                    str]) -> int:
        input_, output = sample
        in_path, out_path, idx = LocalFS.get_new_sample_paths(website, contest_id, task_id)

        with open(in_path, 'w+', encoding='utf-8') as f:
            f.write(input_)
        with open(out_path, 'w+', encoding='utf-8') as f:
            f.write(output)

        return idx

    @staticmethod
    def store_samples(website: Website, contest_id: str, task: Task) -> int:
        LocalFS.delete_samples(website, contest_id, task.id_)
        os.makedirs(LocalFS.get_sample_path(website, contest_id, task.id_, SampleType.IN),
                    exist_ok=True)
        os.makedirs(LocalFS.get_sample_path(website, contest_id, task.id_, SampleType.OUT),
                    exist_ok=True)
        for sample in task.samples:
            LocalFS.store_sample(website, contest_id, task.id_, sample)
        return len(task.samples)

    @staticmethod
    def setup() -> None:
        if not os.path.exists(Config.LUCY_HOME):
            click.echo(f'Creating LUCY_HOME ({Config.LUCY_HOME}).')
            os.makedirs(Config.LUCY_HOME, exist_ok=True)

        if not os.path.exists(Config.SNIPPETS_DIR):
            click.echo(f'Creating SNIPPETS_DIR ({Config.SNIPPETS_DIR}).')
            os.makedirs(Config.SNIPPETS_DIR, exist_ok=True)

        if not os.path.exists(Config.COMMONS_DIR):
            click.echo(f'Creating COMMONS_DIR ({Config.COMMONS_DIR}).')
            os.makedirs(Config.COMMONS_DIR, exist_ok=True)

        if not os.path.exists(Config.TEMPLATE_PATH):
            with open(Config.TEMPLATE_PATH, 'w+', encoding='utf-8'):
                pass

    @staticmethod
    def create_impl_file(website: Website, contest_id: str, task_id: str) -> str:
        impl_path = LocalFS.get_impl_path(website, contest_id, task_id)
        if not os.path.exists(impl_path):
            shutil.copy(Config.TEMPLATE_PATH, impl_path)
        return impl_path

    @staticmethod
    def read(path: str) -> str:
        with open(path) as f:  # pylint: disable=unspecified-encoding
            return f.read()

    @staticmethod
    def tests(website: Website, contest_id: str, task_id: str,
              test_ids: list[int]) -> Generator[Tuple[str, str], None, None]:
        for idx in test_ids:
            in_path = LocalFS.get_sample_path(website, contest_id, task_id, SampleType.IN, idx)
            out_path = LocalFS.get_sample_path(website, contest_id, task_id, SampleType.OUT, idx)
            yield LocalFS.read(in_path), LocalFS.read(out_path)

    @staticmethod
    def parse_active_path() -> Tuple[Optional[str], Optional[str], Optional[str]]:
        site = None
        contest_id = None
        task_id = None

        active_path = os.path.realpath(os.getcwd())
        home_dir = os.path.realpath(Config.LUCY_HOME)
        if active_path.startswith(home_dir):
            active_path = active_path[len(home_dir):]
            active_path = active_path.lstrip('/')

            parts = active_path.split('/')[:3]
            if len(parts) >= 1:
                site = parts[0]
            if len(parts) >= 2:
                contest_id = parts[1]
            if len(parts) >= 3:
                task_id = parts[2]
            if site:
                site = site.lower()

        return site, contest_id, task_id
