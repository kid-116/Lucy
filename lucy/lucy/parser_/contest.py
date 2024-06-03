from typing import Optional

from lucy.config import Website

from lucy.parser_.atcoder import AtCoderParser


class ContestParser:

    def __init__(self,
                 website: Website,
                 contest_id: str,
                 task_id: Optional[str] = None,
                 n_threads: int = 1) -> None:
        self.website = website

        match self.website:
            case Website.ATCODER:
                self.parser = AtCoderParser(contest_id, task_id, n_threads)
            case _:
                raise NotImplementedError()
