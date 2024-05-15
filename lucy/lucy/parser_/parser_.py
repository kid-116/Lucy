from typing import Tuple


class Task:

    def __init__(self, id_: str, name: str, samples: list[Tuple[str, str]]):
        self.id_ = id_
        self.name = name
        self.samples = samples


class Parser:

    def __init__(self, tasks: list[Task]):
        self.tasks = tasks
