'''Run the wsproxy server
'''

# FIXME: uvloop

import asyncio
import logging
import signal
import sys

import click

from wsproxy.server.app import AppRunner

@click.command()
@click.option(
    '--host',
    envvar='WS_PROXY_HOST',
    default='127.0.0.1',
    help='Binding host address. Set to 0.0.0.0 in prod environments',
)
@click.option('--port', envvar='WS_PROXY_PORT', default='8009')
@click.option('--remote_url', envvar='WS_PROXY_REMOTE_URL', default='ws://localhost:8008')
@click.option('--sentry', envvar='WS_PROXY_SENTRY', is_flag=True)
@click.option('--sentry_url', envvar='WS_PROXY_SENTRY_URL')
@click.option('--environment', envvar='WS_PROXY_ENVIRONMENT', default='dev')
def run(host, port, remote_url, sentry, sentry_url, environment):
    '''Main runner'''

    if sentry and sentry_url:
        sentry_sdk.init(
            sentry_url,
            release=getVersion(),
            environment=environment,
            attach_stacktrace=True,
        )

    print('runServer', locals())
    runner = AppRunner(
        host,
        port,
        remote_url,
    )

    loop = asyncio.get_event_loop()
    stop = loop.create_future()

    asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, stop.set_result, None)

    try:
        runner.run(stop)
    except Exception as e:
        logging.fatal(f'Cannot start cobra server: {e}')
        sys.exit(1)
