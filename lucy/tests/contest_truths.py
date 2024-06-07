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

    ABC300 = ContestTruth(Website.ATCODER, 'ABC300', [('A', 6), ('B', 8), ('C', 8), ('D', 4),
                                                      ('E', 8), ('F', 6), ('G', 4), ('Ex', 10)])
