import hashlib
import os
from pathlib import Path
import shutil
from typing import Generator, Optional, Tuple

from lucy.config.config import config
from lucy.types import Contest, SampleType, Task, Test, Website


class LocalFS:

    @staticmethod
    def get_contest_root_dir(contest: Contest) -> Path:
        return config.home / str(contest.site) / contest.contest_id

    @staticmethod
    def get_impl_path(task: Task, dir_: bool = False, bin_: bool = False) -> Path:
        impl_path = LocalFS.get_contest_root_dir(task.contest) / task.task_id
        if bin_:
            return impl_path / config.impl.bin_name
        if not dir_:
            impl_path = impl_path / config.impl.src_name
        return impl_path

    @staticmethod
    def get_sample_path(target: Task | Test, type_: Optional[SampleType] = None) -> Path:
        sample_path = LocalFS.get_impl_path(target.task if isinstance(target, Test) else target,
                                            dir_=True) / config.samples_dir_name
        if type_:
            sample_path = sample_path / str(type_)
            if isinstance(target, Test):
                sample_path = sample_path / f'{target.test_id:02d}.txt'
        return sample_path

    @staticmethod
    def delete_samples(task: Task) -> bool:
        samples_dir = LocalFS.get_sample_path(task)
        if os.path.exists(samples_dir):
            shutil.rmtree(samples_dir)
            return False
        return True

    @staticmethod
    def num_samples(task: Task) -> int:
        if isinstance(task, Test):
            task = task.task
        return len(os.listdir(LocalFS.get_sample_path(task, SampleType.IN)))

    @staticmethod
    def get_new_sample_paths(task: Task) -> Tuple[Path, Path, int]:
        idx = LocalFS.num_samples(task)
        in_path = LocalFS.get_sample_path(Test.from_task(task, idx), SampleType.IN)
        out_path = LocalFS.get_sample_path(Test.from_task(task, idx), SampleType.OUT)
        return in_path, out_path, idx

    @staticmethod
    def store_sample(task: Task, sample: Tuple[str, str]) -> int:
        input_, output = sample
        in_path, out_path, idx = LocalFS.get_new_sample_paths(task)

        with open(in_path, 'w+', encoding='utf-8') as f:
            f.write(input_)
        with open(out_path, 'w+', encoding='utf-8') as f:
            f.write(output)

        return idx

    @staticmethod
    def store_samples(task: Task, samples: list[Tuple[str, str]]) -> int:
        LocalFS.delete_samples(task)
        os.makedirs(LocalFS.get_sample_path(task, SampleType.IN), exist_ok=True)
        os.makedirs(LocalFS.get_sample_path(task, SampleType.OUT), exist_ok=True)
        for sample in samples:
            LocalFS.store_sample(task, sample)
        return len(samples)

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
    def create_impl_file(task: Task) -> Path:
        impl_path = LocalFS.get_impl_path(task)
        if not os.path.exists(impl_path):
            shutil.copy(config.commons.template_path, impl_path)
        return impl_path

    @staticmethod
    def read(path: Path) -> str:
        with open(path) as f:  # pylint: disable=unspecified-encoding
            return f.read()

    @staticmethod
    def load_test(test: Test) -> Tuple[str, str]:
        in_path = LocalFS.get_sample_path(test, SampleType.IN)
        out_path = LocalFS.get_sample_path(test, SampleType.OUT)
        return LocalFS.read(in_path), LocalFS.read(out_path)

    @staticmethod
    def parse_active_path() -> Task:
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

        if not site or not contest_id or not task_id:
            raise ValueError('Not in a task directory.')

        return Task(Website.from_string(site), contest_id, task_id)

    @staticmethod
    def get_impl_hash(task: Task) -> str:
        content = LocalFS.read(LocalFS.get_impl_path(task))
        return hashlib.md5(content.encode()).hexdigest()

    @staticmethod
    def get_snippet_files(path: Path = config.commons.dir_) -> Generator[Path, None, None]:
        for entry in os.scandir(path):
            entry_path = Path(entry.path)
            if entry.is_file():
                yield entry_path
            elif entry.is_dir():
                yield from LocalFS.get_snippet_files(entry_path)

    @staticmethod
    def create_global_snippets_link(force: bool = False) -> bool:
        link_absent = not config.snippets.global_link.exists()
        if link_absent or force:
            if not link_absent:
                os.remove(config.snippets.global_link)
            os.symlink(config.snippets.path, config.snippets.global_link)
        return not link_absent

    @staticmethod
    def get_tmp_file_path(filename: str) -> Path:
        return config.tmp_storage_path / filename

    @staticmethod
    def delete(path: Path) -> None:
        if not path.exists():
            return
        if path.is_dir():
            shutil.rmtree(path)
        else:
            os.remove(path)

    @staticmethod
    def clear() -> None:
        LocalFS.delete(config.tmp_storage_path)
