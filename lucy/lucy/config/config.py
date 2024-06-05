from __future__ import annotations
from dataclasses import dataclass
import os
from pathlib import Path

import dotenv

from lucy.config.commons import CommonsConfig
from lucy.config.impl import ImplConfig
from lucy.config.recent_tests import RecentTestsConfig
from lucy.config.snippets import SnippetsConfig
from lucy.config.test import TestConfig
from lucy.config.user import UserConfig
from lucy.config.website import WebsiteConfig
from lucy.types import Website

dotenv.load_dotenv()


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
                if type_ == str:
                    exec(f"{dest} = '{val}'")  # pylint: disable=exec-used
                else:
                    exec(f'{dest} = type_("{val}")')  # pylint: disable=exec-used

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
            self.n_threads = TestConfig.n_threads


config = ConfigClass()
