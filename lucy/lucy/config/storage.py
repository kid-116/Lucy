from dataclasses import dataclass
import os
from pathlib import Path
import shutil


@dataclass
class StorageConfig:
    tests_dir_name: str = 'tests'
    dir_name: str = '.storage'
    tmp_dir_name: str = 'tmp'
    acl_dir_name: str = 'atcoder'

    @property
    def acl_exists(self) -> bool:
        return self.acl_path.exists() and len(os.listdir(self.acl_path)) > 0

    @property
    def acl_path(self) -> Path:
        return self.path / self.acl_dir_name

    def __init__(self, home: Path) -> None:
        self.path = home / self.dir_name
        self.tmp_path = self.path / self.tmp_dir_name

    def get_tmp_path(self, filename: str) -> Path:
        return self.tmp_path / filename

    def delete_tmp(self, filename: str) -> bool:
        path = self.get_tmp_path(filename)
        if path.exists():
            os.remove(path)
            return True
        return False

    def clear_tmp(self) -> None:
        if self.tmp_path.exists():
            shutil.rmtree(self.tmp_path)
