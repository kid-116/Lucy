from dataclasses import dataclass

from lucy.config import Website


@dataclass
class Task:
    id_: str
    name: str
    num_samples: int


@dataclass
class Contest:
    website: Website
    contest_id: str
    tasks: list[Task]


@dataclass
class AtCoder:
    ABC100 = Contest(Website.ATCODER, 'ABC100', [
        Task('A', 'Happy Birthday!', 6),
        Task('B', 'Ringo\'s Favorite Numbers', 6),
        Task('C', '*3 or /2', 6),
        Task('D', 'Patisserie ABC', 8),
    ])
