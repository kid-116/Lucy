from typing import Any, Generator


def batched(iterable: list[Any], n: int) -> Generator[tuple[Any, ...], None, None]:
    l = len(iterable)
    for ndx in range(0, l, n):
        yield tuple(iterable[ndx:min(ndx + n, l)])
