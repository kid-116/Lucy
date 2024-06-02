import hashlib
import os
from pathlib import Path
import shutil
from typing import Generator, Optional, Tuple

from lucy.config import config, SampleType, Website
from lucy.parser_.parser_ import Task


class LocalFS:

    @staticmethod
    def get_contest_root_dir(website: Website, contest_id: str) -> Path:
        return config.home / str(website) / contest_id

    @staticmethod
    def get_impl_path(website: Website,
                      contest_id: str,
                      task_id: str,
                      dir_: bool = False,
                      bin_: bool = False) -> Path:
        impl_path = LocalFS.get_contest_root_dir(website, contest_id) / task_id
        if bin_:
            return impl_path / config.impl.bin_name
        if not dir_:
            impl_path = impl_path / config.impl.src_name
        return impl_path

    @staticmethod
    def get_sample_path(website: Website,
                        contest_id: str,
                        task_id: str,
                        type_: Optional[SampleType] = None,
                        idx: Optional[int] = None) -> Path:
        sample_path = LocalFS.get_impl_path(website, contest_id, task_id,
                                            dir_=True) / config.samples_dir_name
        if type_:
            sample_path = sample_path / str(type_)
            if idx is not None:
                sample_path = sample_path / f'{idx:02d}.txt'
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
                             task_id: str) -> Tuple[Path, Path, int]:
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
        dir_checks: list[Path] = [
            config.home,
            config.snippets.dir_,
            config.commons.dir_,
            config.storage_path,
        ]

        for dir_ in dir_checks:
            if not dir_.exists():
                os.makedirs(dir_)

        if not os.path.exists(config.commons.template_path):
            with open(config.commons.template_path, 'w+', encoding='utf-8') as template:
                template.write("""#include <iostream>

using namespace std;

int main() {
    return 0;
}
""")

    @staticmethod
    def create_impl_file(website: Website, contest_id: str, task_id: str) -> Path:
        impl_path = LocalFS.get_impl_path(website, contest_id, task_id)
        if not os.path.exists(impl_path):
            shutil.copy(config.commons.template_path, impl_path)
        return impl_path

    @staticmethod
    def read(path: Path) -> str:
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
        home_dir = os.path.realpath(config.home)
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

        return site, contest_id, task_id

    @staticmethod
    def get_impl_hash(website: Website, contest_id: str, task_id: str) -> str:
        content = LocalFS.read(LocalFS.get_impl_path(website, contest_id, task_id))
        return hashlib.md5(content.encode()).hexdigest()
