from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import os

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


class SampleType(Enum):
    IN = 1
    OUT = 2

    def __str__(self) -> str:
        return self.name.lower()


@dataclass
class Config:
    WEBSITE_HOST = {Website.ATCODER: 'https://atcoder.jp'}

    LUCY_HOME = os.getenv('LUCY_HOME') or f'{os.getenv("HOME")}/.lucy'
    LUCY_HOME = os.path.abspath(LUCY_HOME)
    os.makedirs(LUCY_HOME, exist_ok=True)

    SNIPPETS_DIR = f'{LUCY_HOME}/.vscode'
    os.makedirs(SNIPPETS_DIR, exist_ok=True)
    SNIPPETS_PATH = os.path.abspath(f'{SNIPPETS_DIR}/cp.code-snippets')

    COMMONS_PATH = os.path.abspath(f'{LUCY_HOME}/common')
    os.makedirs(COMMONS_PATH, exist_ok=True)

    TEMPLATE_PATH = f'{COMMONS_PATH}/base.cpp'
    if not os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, 'w+', encoding='utf-8'):
            pass

    CLI_WEBSITE_CHOICE = click.Choice(['atcoder'])

    IMPL_MAIN = 'main.cpp'
    IMPL_BIN = 'main'

    SAMPLES_DIR = 'tests'
