from typing import Any, Callable, Generator, Optional, Tuple

import click

from lucy.config import config, Website


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


class Token:

    @staticmethod
    def encode(token: str) -> str:
        return token.replace('%', '?')

    @staticmethod
    def decode(token: str) -> str:
        return token.replace('?', '%')


class Arguments:

    @staticmethod
    def site(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('site', type=click.Choice(Website.choices()), required=required)

    @staticmethod
    def contest_id(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('contest_id',
                              type=str,
                              required=required,
                              callback=to_upper,
                              default=None)

    @staticmethod
    def task_id(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('task_id',
                              type=str,
                              required=required,
                              callback=to_upper,
                              default=None)

    @staticmethod
    def test_id(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('test_id', type=int, required=required, default=None)

    @staticmethod
    def config_key(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('key',
                              type=click.Choice(list(config.user_cfg.configurables.keys())),
                              required=required)

    @staticmethod
    def config_value(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('value', type=str, required=required)


class Options:

    @staticmethod
    def force(help_: str) -> Callable[[Any], Any]:
        return click.option('-f', '--force', 'force', is_flag=True, help=help_, default=False)

    @staticmethod
    def verbose(help_: str = 'Print debug information.') -> Callable[[Any], Any]:
        return click.option('-v', '--verbose', 'verbose', is_flag=True, default=False, help=help_)
