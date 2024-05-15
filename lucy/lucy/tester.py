from __future__ import annotations
import os
import subprocess
from typing import Generator, Tuple

import click

from lucy import utils
from lucy.config import SampleType, Website


# pylint: disable=too-few-public-methods
class Tester:

    def __init__(self, website: Website, contest_id: str, task_id: str, test_id: int) -> None:
        self.website = website
        self.contest_id = contest_id
        self.task_id = task_id

        self.num_tests = len(
            os.listdir(utils.get_sample_path(website, contest_id, task_id, SampleType.IN)))

        if test_id is None:
            self.test_ids = range(self.num_tests)
        else:
            if test_id < 0 or test_id >= self.num_tests:
                raise ValueError("Invalid `test_id`")
            self.test_ids = [test_id]

        self.impl_path = utils.get_impl_path(website, contest_id, task_id)
        self.bin_path = utils.get_impl_path(website, contest_id, task_id, bin_=True)

    def __compile(self) -> None:
        subprocess.check_call(['g++', self.impl_path, '-o', self.bin_path])

    @staticmethod
    def __read(path: str) -> str:
        with open(path) as f:  # pylint: disable=unspecified-encoding
            return f.read()

    def __tests(self) -> Generator[Tuple[int, Tuple[str, str]], None, None]:
        for idx in self.test_ids:
            in_path = utils.get_sample_path(self.website, self.contest_id, self.task_id,
                                            SampleType.IN, idx)
            out_path = utils.get_sample_path(self.website, self.contest_id, self.task_id,
                                             SampleType.OUT, idx)
            yield idx, (Tester.__read(in_path), Tester.__read(out_path))

    def __exec(self, in_txt: str, truth_txt: str) -> bool:
        with subprocess.Popen([self.bin_path], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE) as process:
            assert process.stdin
            process.stdin.write(in_txt.encode())
            process.stdin.close()
            assert process.stdout
            out_txt = process.stdout.read().decode()
            process.wait()
        return out_txt.strip() == truth_txt.strip()

    def run(self) -> None:
        self.__compile()

        for i, (in_txt, out_txt) in self.__tests():
            click.echo(f'Test#{i:02d}', nl=False)
            click.echo(f'{"." * 50}', nl=False)
            passes = self.__exec(in_txt, out_txt)
            if passes:
                click.secho('AC', bg='green')
            else:
                click.secho('WA', bg='red')
