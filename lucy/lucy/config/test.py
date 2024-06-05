from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestConfig:
    home: Path = Path('/tmp/lucy')
    n_threads: int = 1
