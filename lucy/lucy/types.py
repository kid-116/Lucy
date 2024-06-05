from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Union

import click


class Website(Enum):
    ATCODER = 1

    @staticmethod
    def from_string(website: str) -> Website:
        return Website[website.upper()]

    def __str__(self) -> str:
        if self == Website.ATCODER:
            return 'AtCoder'
        raise NotImplementedError()

    @staticmethod
    def choices() -> list[str]:
        return [str(website) for website in Website]


@dataclass
class Contest:
    site: Website
    contest_id: str


@dataclass
class Task(Contest):
    task_id: str

    @property
    def contest(self) -> Contest:
        return Contest(self.site, self.contest_id)

    def __str__(self) -> str:
        return f'{self.site} - {self.contest_id} - {self.task_id}'

    @staticmethod
    def from_contest(contest: Contest, task_id: str) -> Task:
        return Task(contest.site, contest.contest_id, task_id)


@dataclass
class Test(Task):
    test_id: int

    @property
    def task(self) -> Task:
        return Task(self.site, self.contest_id, self.task_id)

    @staticmethod
    def from_task(task: Task, test_id: int) -> Test:
        return Test(task.site, task.contest_id, task.task_id, test_id)


ContestElement = Union[Website, Contest, Task, Test]


class SampleType(Enum):
    IN = 1
    OUT = 2

    def __str__(self) -> str:
        return self.name.lower()


class Token:  # pylint: disable=too-few-public-methods

    def __init__(self, value: str) -> None:
        self.value = value.replace('?', '%')

    def __str__(self) -> str:
        return self.value.replace('%', '?')


class Verdict(Enum):
    AC = 1
    WA = 2

    def __str__(self) -> str:
        return self.name.upper()

    def echo(self) -> None:
        click.secho(str(self), bg='green' if self == Verdict.AC else 'red', bold=True)
