from __future__ import annotations
import subprocess
from typing import Literal, Optional, Tuple, Union

from lucy.types import Task, Test, Verdict


# pylint: disable=too-few-public-methods
class TestingOps:

    def __init__(self, continue_: bool):
        self.continue_ = continue_

    def __compile(self, task: Task) -> None:
        subprocess.check_call(['g++', task.impl_path, '-o', task.bin_path])

    def __exec(self, test: Test, in_txt: str, truth_txt: str) -> Tuple[Verdict, str]:
        with subprocess.Popen([test.task.bin_path], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE) as process:
            assert process.stdin
            process.stdin.write(in_txt.encode())
            process.stdin.close()
            assert process.stdout
            out_txt = process.stdout.read().decode()
            process.wait()
        return Verdict.AC if out_txt.strip() == truth_txt.strip() else Verdict.WA, out_txt

    def run(self, target: Task) -> list[Optional[Union[Literal[Verdict.AC], str]]]:
        self.__compile(target)

        num_tests = target.get_num_tests()
        tests = [target] if isinstance(target,
                                       Test) else [target.get_test(i) for i in range(num_tests)]

        result: list[Optional[Union[Literal[Verdict.AC], str]]] = [None] * num_tests

        for test in tests:
            in_txt, truth_txt = test.load()
            verdict, out_txt = self.__exec(test, in_txt, truth_txt)
            if verdict == Verdict.WA:
                result[test.test_id] = out_txt

                if not self.continue_:
                    break
            else:
                result[test.test_id] = verdict

        return result
