from dataclasses import dataclass

from types_ import ContestTruth

from lucy.config.config import Website


@dataclass
class AtCoder:
    ABC100 = ContestTruth(Website.ATCODER, 'ABC100', [
        ('A', 6),
        ('B', 6),
        ('C', 6),
        ('D', 8),
    ])
