'''wsproxy main test driver.

# flake8: noqa
'''

from pkgutil import walk_packages

import click
import logging

import coloredlogs

LOGGING_FORMAT = '%(asctime)s %(levelname)s %(message)s'
coloredlogs.install(level='WARNING', fmt=LOGGING_FORMAT)


@click.option('--verbose', '-v', envvar='WS_PROXY_VERBOSE', count=True)
@click.group()
@click.version_option()
def main(verbose):
    """\b
wsproxy

wsproxy is a WebSocket proxy server
    """
    if verbose:
        level = 'INFO' if verbose == 1 else 'DEBUG'
        coloredlogs.install(level=level, fmt=LOGGING_FORMAT)


for loader, module_name, is_pkg in walk_packages(__path__, __name__ + '.'):
    module = __import__(module_name, globals(), locals(), ['__name__'])
    cmd = getattr(module, module_name.rsplit('.', 1)[-1])
    if isinstance(cmd, click.Command):
        main.add_command(cmd)
