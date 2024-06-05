from typing import Any, Callable

import click

from lucy.config.config import config


class Options:

    @staticmethod
    def force(help_: str) -> Callable[[Any], Any]:
        return click.option('-f', '--force', 'force', is_flag=True, help=help_, default=False)

    @staticmethod
    def verbose(help_: str = 'Print debug information.') -> Callable[[Any], Any]:
        return click.option('-v', '--verbose', 'verbose', is_flag=True, default=False, help=help_)

    @staticmethod
    def global_(help_: str) -> Callable[[Any], Any]:
        return click.option('-g', '--global', 'global_', default=False, is_flag=True, help=help_)

    @staticmethod
    def n_threads() -> Callable[[Any], Any]:
        return click.option('-t',
                            '--n-threads',
                            'n_threads',
                            default=config.n_threads,
                            type=int,
                            help='Number of execution threads. Warning: Can be flaky!')

    @staticmethod
    def authenticate() -> Callable[[Any], Any]:
        return click.option('-a',
                            '--auth',
                            'auth',
                            is_flag=True,
                            default=False,
                            help='Authenticate.')

    @staticmethod
    def active() -> Callable[[Any], Any]:
        return click.option('-ac',
                            '--active',
                            'active',
                            is_flag=True,
                            default=False,
                            help='Determine target from current directory.')

    @staticmethod
    def continue_(help_: str) -> Callable[[Any], Any]:
        return click.option('-c',
                            '--continue',
                            'continue_',
                            is_flag=True,
                            default=False,
                            help=help_)

    @staticmethod
    def test_id() -> Callable[[Any], Any]:
        return click.option('-ti',
                            '--test-id',
                            'test_id',
                            default=None,
                            type=int,
                            help='Select a specific `test_id`')

    @staticmethod
    def hidden(help_: str) -> Callable[[Any], Any]:
        return click.option('-h', '--hidden', 'hidden', is_flag=True, default=False, help=help_)
