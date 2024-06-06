from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path

import dotenv

from lucy.config.commons import CommonsConfig
from lucy.config.impl import ImplConfig
from lucy.config.recent_tests import RecentTestsConfig
from lucy.config.snippets import SnippetsConfig
from lucy.config.storage import StorageConfig
from lucy.config.test import TestConfig
from lucy.config.user import UserConfig
from lucy.config.website import WebsiteConfig

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

    @property
    def path(self) -> Path:
        return config.home / str(self)


@dataclass
class ConfigClass:  # pylint: disable=too-many-instance-attributes
    home: Path
    snippets: SnippetsConfig
    commons: CommonsConfig
    website: dict[Website, WebsiteConfig]
    recent_tests: RecentTestsConfig
    user_cfg: UserConfig
    storage: StorageConfig
    impl: ImplConfig = ImplConfig()
    n_threads: int = 4
    data_dir: str = 'data'

    def data_path(self, filename: str) -> Path:
        return Path(Path(__file__).parent.parent, self.data_dir, filename)

    @property
    def is_test_env(self) -> bool:
        return 'PYTEST_VERSION' in os.environ

    def __load_user_cfg(self) -> None:
        for key, val in self.user_cfg.gets().items():
            if val:
                dest, type_ = self.user_cfg.configurables[key]
                dest = f'self.{dest}'  # pylint: disable=eval-used
                val = type_(val)
                if type_ == str:
                    exec(f"{dest} = '{val}'")  # pylint: disable=exec-used
                else:
                    exec(f'{dest} = type_("{val}")')  # pylint: disable=exec-used

    def __init__(self) -> None:
        self.home = Path(os.path.abspath(os.getenv('LUCY_HOME') or f'{os.getenv("HOME")}/.lucy'))
        if self.is_test_env:
            self.home = TestConfig.home

        self.storage = StorageConfig(self.home)
        self.user_cfg = UserConfig(self.storage.path)

        self.website = {Website.ATCODER: WebsiteConfig('https://atcoder.jp')}

        self.snippets = SnippetsConfig(self.home)
        self.commons = CommonsConfig(self.home)
        self.recent_tests = RecentTestsConfig(self.storage.path)

        self.__load_user_cfg()

        if self.is_test_env:
            self.n_threads = TestConfig.n_threads


config = ConfigClass()
