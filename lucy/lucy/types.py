from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import hashlib
import os
from pathlib import Path
import shutil
from typing import Tuple, Union

import click

from lucy.config.config import config, Website


@dataclass
class Contest:
    site: Website
    contest_id: str

    def get_task(self, task_id: str) -> Task:
        return Task(self.site, self.contest_id, task_id)

    @property
    def path(self) -> Path:
        return self.site.path / self.contest_id


@dataclass
class Task(Contest):
    task_id: str

    @property
    def contest(self) -> Contest:
        return Contest(self.site, self.contest_id)

    def __str__(self) -> str:
        return f'{self.site} - {self.contest_id} - {self.task_id}'

    @property
    def path(self) -> Path:
        return self.contest.path / self.task_id

    def get_test(self, test_id: int) -> Test:
        return Test(self.site, self.contest_id, self.task_id, test_id)

    @property
    def impl_path(self) -> Path:
        return self.path / config.impl.src_name

    @property
    def bin_path(self) -> Path:
        return self.path / config.impl.bin_name

    def get_num_tests(self) -> int:
        return len(os.listdir(self.test_in_dir))

    @property
    def test_dir(self) -> Path:
        return self.path / config.storage.tests_dir_name

    @property
    def test_in_dir(self) -> Path:
        return self.test_dir / str(SampleType.IN)

    @property
    def test_out_dir(self) -> Path:
        return self.test_dir / str(SampleType.OUT)

    def new_test_path(self) -> Tuple[Path, Path]:
        test = self.get_test(self.get_num_tests())
        return test.get_path(SampleType.IN), test.get_path(SampleType.OUT)

    def delete_tests(self) -> bool:
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
            return True
        return False

    def store_test(self, test_txt: Tuple[str, str]) -> int:
        os.makedirs(self.test_in_dir, exist_ok=True)
        os.makedirs(self.test_out_dir, exist_ok=True)
        in_txt, out_txt = test_txt
        test = self.get_test(self.get_num_tests())
        with open(test.in_path, 'w+', encoding='utf-8') as f:
            f.write(in_txt)
        with open(test.out_path, 'w+', encoding='utf-8') as f:
            f.write(out_txt)
        return test.test_id

    def store_tests(self, test_txts: list[Tuple[str, str]]) -> int:
        for test_txt in test_txts:
            self.store_test(test_txt)
        return len(test_txts)

    @property
    def acl_path(self) -> Path:
        return self.path / config.storage.acl_dir_name

    def create_impl_file(self) -> Path:
        if not self.impl_path.exists():
            if not self.path.exists():
                os.makedirs(self.path)
            shutil.copy(config.commons.template_path, self.impl_path)
        if not self.acl_path.exists():
            os.symlink(config.storage.acl_path, self.acl_path, target_is_directory=True)
        return self.impl_path

    def get_impl_hash(self) -> str:
        return hashlib.md5(self.impl_path.read_text().encode()).hexdigest()

    def exists(self) -> bool:
        return self.impl_path.exists() and self.test_dir.exists() and self.test_in_dir.exists(
        ) and self.test_out_dir.exists()


@dataclass
class Test(Task):
    test_id: int

    @property
    def task(self) -> Task:
        return Task(self.site, self.contest_id, self.task_id)

    def get_path(self, type_: SampleType) -> Path:
        return self.test_dir / str(type_) / f'{self.test_id:02d}.txt'

    def rename(self, new_test_id: int) -> None:
        new_test = self.task.get_test(new_test_id)
        os.rename(self.in_path, new_test.in_path)
        os.rename(self.out_path, new_test.out_path)
        self.test_id = new_test_id

    def delete(self) -> None:
        assert self.in_path.exists()
        os.remove(self.in_path)
        os.remove(self.out_path)
        for i in range(self.test_id + 1, self.task.get_num_tests()):
            self.task.get_test(i).rename(i - 1)

    @property
    def in_path(self) -> Path:
        return self.get_path(SampleType.IN)

    @property
    def out_path(self) -> Path:
        return self.get_path(SampleType.OUT)

    def load(self) -> Tuple[str, str]:
        return self.in_path.read_text().strip(), self.out_path.read_text().strip()


ContestElement = Union[Website, Contest, Task, Test]


class SampleType(Enum):
    IN = 1
    OUT = 2

    def __str__(self) -> str:
        return self.name.lower()


class Verdict(Enum):
    AC = 1
    WA = 2

    def __str__(self) -> str:
        return self.name.upper()

    def echo(self) -> None:
        click.secho(str(self), bg='green' if self == Verdict.AC else 'red', bold=True)
