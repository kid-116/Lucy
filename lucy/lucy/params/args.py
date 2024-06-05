from typing import Any, Callable, Optional

import click

from lucy.config.config import config
from lucy.types import Website


class Arguments:

    @staticmethod
    def __to_upper(_ctx: Any, _param: Any, value: Optional[str]) -> Optional[str]:
        if isinstance(value, str):
            return value.upper()
        return value

    @staticmethod
    def site(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('site', type=click.Choice(Website.choices()), required=required)

    @staticmethod
    def contest_id(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('contest_id',
                              type=str,
                              required=required,
                              callback=Arguments.__to_upper,
                              default=None)

    @staticmethod
    def task_id(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('task_id',
                              type=str,
                              required=required,
                              callback=Arguments.__to_upper,
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
