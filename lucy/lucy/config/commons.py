from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommonsConfig:
    dir_: Path
    template_file_name: str = 'base.cpp'
    dir_name: str = 'common'

    def __init__(self, home: Path) -> None:
        self.dir_ = home / self.dir_name

    @property
    def template_path(self) -> Path:
        return self.dir_ / self.template_file_name
