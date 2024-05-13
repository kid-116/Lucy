class Task:

    def __init__(self, id_: str, name: str):
        self.id_ = id_
        self.name = name


class Parser:

    def __init__(self, tasks: list[Task]):
        self.tasks = tasks

    def tasks(self) -> list[Task]:
        return self.tasks
