from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Website(Enum):
    ATCODER = 1

    @staticmethod
    def from_string(website: str) -> Website:
        return Website[website.upper()]

    def __str__(self) -> str:
        if self == Website.ATCODER:
            return 'AtCoder'
        raise NotImplementedError()


@dataclass
class Config:
    WEBSITE_HOST = {Website.ATCODER: 'https://atcoder.jp'}
