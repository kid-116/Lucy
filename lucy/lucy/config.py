from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path

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

    @staticmethod
    def choices() -> list[str]:
        return [str(website) for website in Website]


class SampleType(Enum):
    IN = 1
    OUT = 2

    def __str__(self) -> str:
        return self.name.lower()


@dataclass
class SnippetsConfig:
    dir_: Path
    file_name: str

    def __init__(self, home: Path) -> None:
        self.dir_ = home / '.vscode'
        self.file_name = 'cp.code-snippets'

    @property
    def path(self) -> Path:
        return self.dir_ / self.file_name


@dataclass
class CommonsConfig:
    dir_: Path
    template_file_name: str = 'base.cpp'

    def __init__(self, home: Path) -> None:
        self.dir_ = home / 'common'

    @property
    def template_path(self) -> Path:
        return self.dir_ / self.template_file_name


@dataclass
class ImplConfig:
    src_name: str = 'main.cpp'
    bin_name: str = 'main'


@dataclass
class TestConfig:
    home: Path = Path('/tmp/lucy')


@dataclass
class ConfigClass:
    home: Path
    snippets: SnippetsConfig
    commons: CommonsConfig
    impl: ImplConfig
    host: dict[Website, str]
    samples_dir_name: str = 'tests'

    def __init__(self) -> None:
        home = os.path.abspath(os.getenv('LUCY_HOME') or f'{os.getenv("HOME")}/.lucy')
        if 'PYTEST_VERSION' in os.environ:
            home = TestConfig.home
        self.home = Path(home)
        del home
        self.host = {Website.ATCODER: 'https://atcoder.jp'}
        self.snippets = SnippetsConfig(self.home)
        self.commons = CommonsConfig(self.home)
        self.impl = ImplConfig()


config = ConfigClass()
