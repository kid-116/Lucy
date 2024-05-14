from lucy.config import Website

from lucy.parser_.atcoder import AtCoderParser


class Contest:

    def __init__(self, website: Website, contest_id: str) -> None:
        self.website = website

        match self.website:
            case Website.ATCODER:
                self.parser = AtCoderParser(contest_id.lower())
            case _:
                raise NotImplementedError()
