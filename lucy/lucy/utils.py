from typing import Any, Generator, Optional

from lucy.config import Config, SampleType, Website


def batched(iterable: list[Any], n: int) -> Generator[tuple[Any, ...], None, None]:
    l = len(iterable)
    for ndx in range(0, l, n):
        yield tuple(iterable[ndx:min(ndx + n, l)])


def get_impl_path(website: Website,
                  contest_id: str,
                  task_id: str,
                  dir_: bool = False,
                  bin_: bool = False) -> str:
    impl_path = f'{Config.LUCY_HOME}/{website}/{contest_id.upper()}/{task_id.upper()}'
    if bin_:
        return f'{impl_path}/{Config.IMPL_BIN}'
    if not dir_:
        impl_path = f'{impl_path}/{Config.IMPL_MAIN}'
    return impl_path


def get_sample_path(website: Website,
                    contest_id: str,
                    task_id: str,
                    type_: Optional[SampleType] = None,
                    idx: Optional[int] = None) -> str:
    sample_path = get_impl_path(website, contest_id, task_id, dir_=True)
    sample_path += f'/{Config.SAMPLES_DIR}'
    if type_:
        sample_path += f'/{type_}'
        if idx is not None:
            sample_path += f'/{idx:02d}.txt'
    return sample_path
