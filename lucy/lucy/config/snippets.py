import os

from dataclasses import dataclass
from pathlib import Path


@dataclass
class SnippetsConfig:
    dir_: Path
    file_name: str = 'cp.code-snippets'

    @property
    def global_link(self) -> Path:
        return Path(f'{os.getenv("HOME")}/.config/Code/User/snippets/{self.file_name}')

    def __init__(self, home: Path) -> None:
        self.dir_ = home / '.vscode'

    @property
    def path(self) -> Path:
        return self.dir_ / self.file_name
