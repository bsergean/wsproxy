A simple python websocket proxy, with per message deflate compression support
unlike nginx, apache or haproxy which just proxy at the TCP level. Alpha
quality, *not* battle-tested, a quick but functional experiment.

# Usage

## Running a regular websocket echo server, with zlib compression disabled.

```
$ ws echo_server -x
[2020-02-26 10:16:14.460] [info] Listening on 127.0.0.1:8008
[2020-02-26 10:16:14.460] [info] Disable per message deflate
```

## Running the wsproxy server, proxying to ws://localhost:8008

```
(venv) ws_proxy$ wsproxy --version
wsproxy, version 0.0.1
(venv) ws_proxy$ wsproxy
Usage: wsproxy [OPTIONS] COMMAND [ARGS]...

  wsproxy

  wsproxy is a WebSocket proxy server

Options:
  --version      Show the version and exit.
  -v, --verbose
  --help         Show this message and exit.

Commands:
  run  Main runner
(venv) ws_proxy$ wsproxy run
runServer {'host': '127.0.0.1', 'port': '8009', 'remote_url': 'ws://localhost:8008', 'sentry': False, 'sentry_url': None, 'environment': 'dev'}
```

## Running a ws echo client, connecting to the proxy server

The server header response contains `Sec-WebSocket-Extensions: permessage-deflate; server_max_window_bits=15; client_max_window_bits=15`, which means compression is enabled between the client and the proxy.

```
$ ws connect ws://localhost:8009
Type Ctrl-D to exit prompt...
Connecting to url: ws://localhost:8009
> ws_connect: connected
[2020-02-26 10:18:57.991] [info] Uri: /
[2020-02-26 10:18:57.992] [info] Headers:
[2020-02-26 10:18:57.992] [info] Connection: Upgrade
[2020-02-26 10:18:57.992] [info] Date: Wed, 26 Feb 2020 18:18:57 GMT
[2020-02-26 10:18:57.992] [info] Sec-WebSocket-Accept: St09vq7bqY73/JUCl++dC+wpgxI=
[2020-02-26 10:18:57.992] [info] Sec-WebSocket-Extensions: permessage-deflate; server_max_window_bits=15; client_max_window_bits=15
[2020-02-26 10:18:57.992] [info] Server: Python/3.8 websockets/8.1
[2020-02-26 10:18:57.992] [info] Upgrade: websocket
hello
> [2020-02-26 10:19:01.115] [info] Received 8 bytes
ws_connect: received message: hello
world
> [2020-02-26 10:19:02.954] [info] Received 7 bytes
ws_connect: received message: world
```

# Dependencies

* python websocket [library](https://websockets.readthedocs.io/en/stable/).

