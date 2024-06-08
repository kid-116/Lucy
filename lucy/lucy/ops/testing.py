from __future__ import annotations
import subprocess
from typing import Any, Literal, Optional, Tuple, Union

import termcolor

from lucy.types import Task, Test, Verdict


# pylint: disable=too-few-public-methods
class TestingOps:

    def __init__(self, continue_: bool = False):
        self.continue_ = continue_

    def __compile(self, task: Task) -> None:
        subprocess.check_call(
            ['g++', task.impl_path, '-o', task.bin_path, '--std=c++17', '-I', task.path])

    def __exec(self, test: Test, in_txt: str, truth_txt: str) -> Tuple[Verdict, str]:
        with subprocess.Popen([test.task.bin_path], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE) as process:
            assert process.stdin
            process.stdin.write(in_txt.encode())
            process.stdin.close()
            assert process.stdout
            out_txt = process.stdout.read().decode()
            process.wait()
        return Verdict.AC if out_txt.strip() == truth_txt.strip() else Verdict.WA, out_txt.strip()

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


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class DiffOps:

    def __init__(self, txt: str, truth: str):
        self.txt = txt
        self.truth = truth

    def __make_eq_len(self, a: list[Any], b: list[Any]) -> None:
        while len(a) < len(b):
            a.append(None)
        while len(b) < len(a):
            b.append(None)

    def print(self) -> None:
        txt_lines = self.txt.splitlines()
        truth_lines = self.truth.splitlines()
        self.__make_eq_len(txt_lines, truth_lines)
        for txt_line, truth_line in zip(txt_lines, truth_lines):
            self.__print_line(txt_line, truth_line)

    def __print_line(self, txt: Optional[str], truth: Optional[str]) -> None:
        if txt is None:
            print(termcolor.colored('(+)', 'yellow'))
            return
        if truth is None:
            print(termcolor.colored(f'{txt} (-)', 'red'))
            return
        truth_tokens = truth.split(' ')
        txt_tokens = txt.split(' ')
        self.__make_eq_len(txt_tokens, truth_tokens)
        for txt_token, truth_token in zip(txt_tokens, truth_tokens):
            self.__print_token(txt_token, truth_token)
        print()

    def __print_token(self, txt: Optional[str], truth: Optional[str]) -> None:
        if txt is None:
            print(termcolor.colored('?', 'yellow'))
            return
        if truth is None:
            print(termcolor.colored(f'~{txt}', 'yellow'), end=' ')
            return
        if txt == truth:
            print(termcolor.colored(txt, 'green'), end=' ')
        else:
            print(termcolor.colored(txt, 'red'), end=' ')


# pylint: enable=too-few-public-methods
