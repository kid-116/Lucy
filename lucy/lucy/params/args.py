from typing import Any, Callable

import click

from lucy.config.config import config, Website


class Arguments:

    @staticmethod
    def site(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('site', type=click.Choice(Website.choices()), required=required)

    @staticmethod
    def contest_id(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('contest_id', type=str, required=required, default=None)

    @staticmethod
    def task_id(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('task_id', type=str, required=required, default=None)

    @staticmethod
    def test_id(required: bool = False, type_: type = int) -> Callable[[Any], Any]:
        return click.argument('test_id', type=type_, required=required, default=None)

    @staticmethod
    def config_key(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('key',
                              type=click.Choice(list(config.user_cfg.configurables.keys())),
                              required=required)

    @staticmethod
    def config_value(required: bool = False) -> Callable[[Any], Any]:
        return click.argument('value', type=str, required=required)

    @staticmethod
    def version(default: str) -> Callable[[Any], Any]:
        return click.argument('version', type=str, required=False, default=default)
