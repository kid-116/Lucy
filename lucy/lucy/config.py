from __future__ import annotations
from configparser import ConfigParser
from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path
import shelve
from shelve import Shelf
from typing import Optional, Tuple

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

    @property
    def global_link(self) -> Path:
        return Path(f'{os.getenv("HOME")}/.config/Code/User/snippets/{self.file_name}')

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
class RecentTestsConfig:
    dir_: Path
    file_name: str = 'recent_tests'
    warning_msg: str = 'Warning: Unchanged solution!'

    @property
    def path(self) -> Path:
        return self.dir_ / self.file_name

    def get_cache(self) -> Shelf[str]:
        return shelve.open(str(self.path))

    def __init__(self, storage_path: Path) -> None:
        self.dir_ = storage_path


@dataclass
class WebsiteConfig:
    host: str
    user_id: Optional[str] = None
    passwd: Optional[str] = None
    token: Optional[str] = None
    auth_token_name: str = 'REVEL_SESSION'
    login_path: str = 'login'
    protected_path: str = 'settings'

    @property
    def login_url(self) -> str:
        return f'{self.host}/{self.login_path}'

    @property
    def protected_url(self) -> str:
        return f'{self.host}/{self.protected_path}'


@dataclass
class UserConfig:
    configurables: dict[str, Tuple[str, type]]
    dir_: Path
    cfg_file_name: str = 'overrides.cfg'
    cfg_default_section: str = 'DEFAULT'

    @property
    def path(self) -> Path:
        return self.dir_ / self.cfg_file_name

    def __init__(self, storage_path: Path) -> None:
        self.dir_ = storage_path
        self.cfg = ConfigParser()
        self.cfg.read(self.path)
        self.cfg_default = self.cfg[self.cfg_default_section]
        self.configurables = {
            'AtCoder.UserId': ('website[Website.ATCODER].user_id', str),
            'AtCoder.Password': ('website[Website.ATCODER].passwd', str),
            'AtCoder.Token': ('website[Website.ATCODER].token', str),
            'NThreads': ('n_threads', int),
        }

    def gets(self) -> dict[str, Optional[str]]:
        return {key: self.get(key) for key in self.configurables}

    def save(self) -> None:
        with open(self.path, 'w') as cfg_file:  # pylint: disable=unspecified-encoding
            self.cfg.write(cfg_file)

    def get(self, key: str) -> Optional[str]:
        return self.cfg_default.get(key)

    def set(self, key: str, val: str) -> None:
        self.cfg_default[key] = val
        self.save()

    def unset(self, key: str) -> None:
        self.cfg_default.pop(key, None)
        self.save()


@dataclass
class ConfigClass:  # pylint: disable=too-many-instance-attributes
    home: Path
    snippets: SnippetsConfig
    commons: CommonsConfig
    website: dict[Website, WebsiteConfig]
    recent_tests: RecentTestsConfig
    user_cfg: UserConfig
    impl: ImplConfig = ImplConfig()
    samples_dir_name: str = 'tests'
    storage_dir_name: str = '.storage'
    n_threads: int = 4

    @property
    def storage_path(self) -> Path:
        return self.home / self.storage_dir_name

    def __load_user_cfg(self) -> None:
        for key, val in self.user_cfg.gets().items():
            if val:
                dest, type_ = self.user_cfg.configurables[key]
                dest = f'self.{dest}'  # pylint: disable=eval-used
                val = type_(val)
                if isinstance(val, str):
                    exec(f"{dest} = '{val}'")  # pylint: disable=exec-used
                else:
                    exec(f'{dest} = {val}')  # pylint: disable=exec-used

    def __init__(self) -> None:
        self.home = Path(os.path.abspath(os.getenv('LUCY_HOME') or f'{os.getenv("HOME")}/.lucy'))
        if 'PYTEST_VERSION' in os.environ:
            self.home = TestConfig.home

        self.user_cfg = UserConfig(self.storage_path)

        self.website = {Website.ATCODER: WebsiteConfig('https://atcoder.jp')}

        self.snippets = SnippetsConfig(self.home)
        self.commons = CommonsConfig(self.home)
        self.recent_tests = RecentTestsConfig(self.storage_path)

        self.__load_user_cfg()

        if 'PYTEST_VERSION' in os.environ:
            self.n_threads = 1


config = ConfigClass()
