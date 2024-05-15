from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import os

import click
import dotenv

dotenv.load_dotenv()


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

    SNIPPETS_DIR = f'{LUCY_HOME}/.vscode'
    SNIPPETS_PATH = f'{SNIPPETS_DIR}/cp.code-snippets'

    COMMONS_DIR = os.path.abspath(f'{LUCY_HOME}/common')

    TEMPLATE_PATH = f'{COMMONS_DIR}/base.cpp'

    CLI_WEBSITE_CHOICE = click.Choice(['atcoder'])

    IMPL_MAIN = 'main.cpp'
    IMPL_BIN = 'main'

    SAMPLES_DIR = 'tests'

    DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')

    # pylint: disable=line-too-long
    ATCODER_TESTCASES_DROPBOX_LINK = 'https://www.dropbox.com/sh/nx3tnilzqz7df8a/AAAYlTq2tiEHl5hsESw6-yfLa?dl=0'
    # pylint: enable=line-too-long
