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
    assert os.path.isdir(LUCY_HOME)

    SNIPPETS_DIR = f'{LUCY_HOME}/.vscode'
    SNIPPETS_FILE_NAME = 'cp.code-snippets'
    SNIPPETS_PATH = f'{SNIPPETS_DIR}/{SNIPPETS_FILE_NAME}'

    COMMONS_DIR = os.path.abspath(f'{LUCY_HOME}/common')

    TEMPLATE_PATH = f'{COMMONS_DIR}/base.cpp'

    CLI_WEBSITE_CHOICE = click.Choice(['atcoder'])

    IMPL_MAIN = 'main.cpp'
    IMPL_BIN = 'main'

    SAMPLES_DIR = 'tests'

    # pylint: disable=line-too-long
    DROPBOX_TOKEN = os.getenv(
        'DROPBOX_TOKEN'
    ) or 'sl.B1Rp-zCsGfT8Pd3K_LSV-CduAGyJrBbltWKlly2JvHDzRf3u9AG68md6obRbVyoygMgytF_2L5SYoLijtyQ99qsHH9d9r1SdomNlWZk7uyPTpN4TxhtvnRlbuEfXfpGPF285E61xlXNz'

    ATCODER_TESTCASES_DROPBOX_LINK = 'https://www.dropbox.com/sh/nx3tnilzqz7df8a/AAAYlTq2tiEHl5hsESw6-yfLa?dl=0'
    # pylint: enable=line-too-long
