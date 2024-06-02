from typing import Any, Generator, Optional, Tuple


def batched(iterable: list[Any], n: int) -> Generator[tuple[Any, ...], None, None]:
    l = len(iterable)
    for ndx in range(0, l, n):
        yield tuple(iterable[ndx:min(ndx + n, l)])


def hash_(tuple_: Tuple[Any, ...]) -> str:
    return '-'.join(str(x) for x in tuple_)


def to_upper(_ctx: Any, _param: Any, value: Optional[str]) -> Optional[str]:
    if isinstance(value, str):
        return value.upper()
    return value
