from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import os
from typing import Optional

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

    LUCY_ROOT = '.lucy'
    LUCY_HOME = os.getenv('LUCY_HOME') or f'{os.path.dirname(__file__)}/../../'
    LUCY_HOME = os.path.abspath(LUCY_HOME)
    LUCY_STORAGE = os.path.abspath(f'{LUCY_HOME}/{LUCY_ROOT}')

    SNIPPETS_PATH = os.path.abspath(f'{LUCY_HOME}/.vscode/cp.code-snippets')
    COMMONS_PATH = os.path.abspath(f'{LUCY_HOME}/common')

    TEMPLATE_PATH = f'{COMMONS_PATH}/base.cpp'

    CLI_WEBSITE_CHOICE = click.Choice(['atcoder'])

    IMPLEMENTATION_MAIN = 'main.cpp'
    COMPLILED_FILE_NAME = 'main'

    @staticmethod
    def get_sample_path(website: Website, contest_id: str, task_id: str, type_: SampleType,
                        idx: int) -> str:
        return f'{Config.get_samples_root(website, contest_id, task_id, type_)}/{type_}{idx:02d}.txt'

    @staticmethod
    def get_samples_root(website: Website,
                         contest_id: str,
                         task_id: Optional[str] = None,
                         sample_type: Optional[SampleType] = None) -> str:
        samples_root = f'{Config.LUCY_STORAGE}/{website}/{contest_id.lower()}'
        if task_id:
            samples_root += f'/{task_id}'
            if sample_type:
                samples_root += f'/{sample_type}'
        return samples_root

    @staticmethod
    def get_implementation_root(website: Website,
                                contest_id: str,
                                task_id: Optional[str] = None) -> str:
        implementation_root = f'{Config.LUCY_HOME}/{website}/{contest_id.upper()}'
        if task_id:
            implementation_root += f'/{task_id}'
        return implementation_root

    @staticmethod
    def get_implementation_path(website: Website, contest_id: str, task_id: str) -> str:
        return f'{Config.get_implementation_root(website, contest_id)}/{task_id}/{Config.IMPLEMENTATION_MAIN}'
