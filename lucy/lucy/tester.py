from __future__ import annotations
import subprocess
from typing import Optional, Tuple

import click

from lucy.config import Website
from lucy.filesystem import LocalFS


# pylint: disable=too-few-public-methods
class Tester:

    def __init__(self, website: Website, contest_id: str, task_id: str,
                 test_id: Optional[int]) -> None:
        self.website = website
        self.contest_id = contest_id
        self.task_id = task_id

        self.num_tests = LocalFS.num_samples(website, contest_id, task_id)

        self.test_ids: list[int] = list(range(self.num_tests))
        if test_id is not None:
            if test_id < 0 or test_id >= self.num_tests:
                raise ValueError("Invalid `test_id`")
            self.test_ids = [test_id]

        self.impl_path = LocalFS.get_impl_path(website, contest_id, task_id)
        self.bin_path = LocalFS.get_impl_path(website, contest_id, task_id, bin_=True)

    def __compile(self) -> None:
        subprocess.check_call(['g++', self.impl_path, '-o', self.bin_path])

    def __exec(self, in_txt: str, truth_txt: str) -> Tuple[bool, str]:
        with subprocess.Popen([self.bin_path], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE) as process:
            assert process.stdin
            process.stdin.write(in_txt.encode())
            process.stdin.close()
            assert process.stdout
            out_txt = process.stdout.read().decode()
            process.wait()
        return out_txt.strip() == truth_txt.strip(), out_txt

    def run(self, verbose: bool = False, continue_: bool = False) -> None:
        self.__compile()

        for i, (in_txt, truth_txt) in zip(
                self.test_ids,
                LocalFS.tests(self.website, self.contest_id, self.task_id, self.test_ids)):
            click.echo(f'Test#{i:02d}', nl=False)
            click.echo(f'{"." * 50}', nl=False)
            passes, out_txt = self.__exec(in_txt, truth_txt)
            if passes:
                click.secho('AC', bg='green')
            else:
                click.secho('WA', bg='red')
                if verbose:
                    click.secho("Input:", bg='white', bold=True)
                    print(in_txt.strip())
                    click.secho("Output:", bg='red', bold=True)
                    print(out_txt.strip())
                    click.secho("Expected:", bg='green', bold=True)
                    print(truth_txt.strip())
                if not continue_:
                    break
