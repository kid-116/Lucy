from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Tuple

from lucy.types import Token


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
            'AtCoder.Token': ('website[Website.ATCODER].token', Token),
            'NThreads': ('n_threads', int),
        }

    def gets(self) -> dict[str, Optional[str]]:
        return {key: self.get(key) for key in self.configurables}

    def save(self) -> None:
        with open(self.path, 'w') as cfg_file:  # pylint: disable=unspecified-encoding
            self.cfg.write(cfg_file)

    def get(self, key: str) -> Optional[str]:
        return self.cfg_default.get(key)

    def set(self, key: str, val: Any) -> None:
        self.cfg_default[key] = str(val)
        self.save()

    def unset(self, key: str) -> None:
        self.cfg_default.pop(key, None)
        self.save()
