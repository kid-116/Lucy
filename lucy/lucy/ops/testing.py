from __future__ import annotations
import subprocess
from typing import Tuple

import click

from lucy.filesystem import LocalFS
from lucy.types import Task, Test, Verdict


# pylint: disable=too-few-public-methods
class TestingOps:

    @staticmethod
    def __compile(target: Task) -> None:
        impl_path = LocalFS.get_impl_path(target)
        bin_path = LocalFS.get_impl_path(target, bin_=True)
        subprocess.check_call(['g++', impl_path, '-o', bin_path])

    @staticmethod
    def __exec(target: Test, in_txt: str, truth_txt: str) -> Tuple[Verdict, str]:
        bin_path = LocalFS.get_impl_path(target, bin_=True)
        with subprocess.Popen([bin_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
            assert process.stdin
            process.stdin.write(in_txt.encode())
            process.stdin.close()
            assert process.stdout
            out_txt = process.stdout.read().decode()
            process.wait()
        return Verdict.AC if out_txt.strip() == truth_txt.strip() else Verdict.WA, out_txt

    @staticmethod
    def run(target: Task | Test, verbose: bool = False, continue_: bool = False) -> None:
        TestingOps.__compile(target)

        num_tests = LocalFS.num_samples(target)
        tests = [target] if isinstance(
            target, Test) else [Test.from_task(target, i) for i in range(num_tests)]

        for test in tests:
            click.echo(f'Test#{test.test_id:02d}/{num_tests - 1:02d}', nl=False)
            click.echo(f'{"." * 50}', nl=False)
            in_txt, truth_txt = LocalFS.load_test(test)
            verdict, out_txt = TestingOps.__exec(test, in_txt, truth_txt)
            verdict.echo()
            if verdict == Verdict.WA:
                if verbose:
                    click.secho("Input:", bg='white', bold=True)
                    print(in_txt.strip())
                    click.secho("Output:", bg='red', bold=True)
                    print(out_txt.strip())
                    click.secho("Expected:", bg='green', bold=True)
                    print(truth_txt.strip())
                if not continue_:
                    break
