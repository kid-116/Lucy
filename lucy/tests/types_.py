from dataclasses import dataclass
from typing import Tuple

from lucy.types import Contest, Task, Website


@dataclass
class TaskTruth(Task):
    num_samples: int


@dataclass
class ContestTruth(Contest):
    tasks: list[TaskTruth]

    def __init__(self, website: Website, contest_id: str, task_details: list[Tuple[str, int]]):
        self.site = website
        self.contest_id = contest_id
        self.tasks = [
            TaskTruth(website, contest_id, task_id, num_samples)
            for task_id, num_samples in task_details
        ]
        super().__init__(website, contest_id)
