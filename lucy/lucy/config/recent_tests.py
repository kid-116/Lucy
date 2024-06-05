from dataclasses import dataclass
from pathlib import Path
import shelve
from shelve import Shelf


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
