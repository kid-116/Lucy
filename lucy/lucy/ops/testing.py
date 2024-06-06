from __future__ import annotations
import subprocess
from typing import Literal, Optional, Tuple, Union

from lucy.filesystem import LocalFS
from lucy.types import Task, Test, Verdict


# pylint: disable=too-few-public-methods
class TestingOps:

    def __init__(self, verbose: bool, continue_: bool):
        # self.verbose = verbose
        self.continue_ = continue_

    def __compile(self, target: Task) -> None:
        impl_path = LocalFS.get_impl_path(target)
        bin_path = LocalFS.get_impl_path(target, bin_=True)
        subprocess.check_call(['g++', impl_path, '-o', bin_path])

    def __exec(self, target: Test, in_txt: str, truth_txt: str) -> Tuple[Verdict, str]:
        bin_path = LocalFS.get_impl_path(target, bin_=True)
        with subprocess.Popen([bin_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
            assert process.stdin
            process.stdin.write(in_txt.encode())
            process.stdin.close()
            assert process.stdout
            out_txt = process.stdout.read().decode()
            process.wait()
        return Verdict.AC if out_txt.strip() == truth_txt.strip() else Verdict.WA, out_txt

    def run(self, target: Task) -> list[Optional[Union[Literal[Verdict.AC], str]]]:
        self.__compile(target)

        num_tests = LocalFS.num_samples(target)
        tests = [target] if isinstance(
            target, Test) else [Test.from_task(target, i) for i in range(num_tests)]

        result: list[Optional[Union[Literal[Verdict.AC], str]]] = [None] * num_tests

        for test in tests:
            in_txt, truth_txt = LocalFS.load_test(test)
            verdict, out_txt = self.__exec(test, in_txt, truth_txt)
            if verdict == Verdict.WA:
                result[test.test_id] = out_txt
                
                if not self.continue_:
                    break
            else:
                result[test.test_id] = verdict

        return result
