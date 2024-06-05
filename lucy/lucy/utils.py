from typing import Any, Generator, Optional, Tuple

from lucy.types import Contest, ContestElement, Task, Test, Website


def batched(iterable: list[Any], n: int) -> Generator[tuple[Any, ...], None, None]:
    l = len(iterable)
    for ndx in range(0, l, n):
        yield tuple(iterable[ndx:min(ndx + n, l)])


def hash_(tuple_: Tuple[Any, ...]) -> str:
    return '-'.join(str(x) for x in tuple_)


def build(site_str: Optional[str] = None,
          contest_id: Optional[str] = None,
          task_id: Optional[str] = None,
          test_id: Optional[int] = None) -> Optional[ContestElement]:
    if not site_str:
        return None
    site = Website.from_string(site_str)
    if not contest_id:
        return site
    if not task_id:
        return Contest(site, contest_id)
    if not test_id:
        return Task(site, contest_id, task_id)
    return Test(site, contest_id, task_id, test_id)
