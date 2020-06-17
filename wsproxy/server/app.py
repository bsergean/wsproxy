'''Main entry point for the server
'''
import asyncio
import functools
import http
import importlib
import logging
import traceback
import json
import zlib

import websockets
from wsproxy.common.version import getVersion
from wsproxy.common.banner import getBanner


async def clientToServer(ws, websocket):
    async for message in ws:
        await websocket.send(message)


async def serverToClient(ws, websocket):
    async for message in websocket:
        await ws.send(message)


async def msgHandler(websocket, path, remoteUrl: str):
    '''Called whenever a new connection is made to the server'''
    userAgent = websocket.requestHeaders.get('User-Agent', 'unknown-user-agent')

    # For debugging
    websocket.userAgent = userAgent

    taskA = None
    taskB = None

    try:
        url = remoteUrl + path
        async with websockets.connect(url) as ws:
            taskA = asyncio.create_task(clientToServer(ws, websocket))
            taskB = asyncio.create_task(serverToClient(ws, websocket))

            await taskA
            await taskB

    except websockets.exceptions.ProtocolError as e:
        print(e)
        print('Protocol error')
    except websockets.exceptions.ConnectionClosedOK:
        print('Connection closed properly')
    except websockets.exceptions.ConnectionClosedError:
        print('Connection closed with an error')
    except Exception as e:
        print(e)
        print('Generic Exception caught in {}'.format(traceback.format_exc()))
    finally:
        # cancel both tasks
        if taskA is not None:
            taskA.cancel()

        if taskB is not None:
            taskB.cancel()


class ServerProtocol(websockets.WebSocketServerProtocol):
    requestHeaders = None

    async def process_request(self, path, request_headers):
        self.requestHeaders = request_headers
        return await super().process_request(path, request_headers)

    async def read_message(self):
        try:
            return await super().read_message()
        except zlib.error as e:
            headers = json.dumps({k: v for (k, v) in self.requestHeaders.raw_items()})
            logging.error(
                'Error in zlib for %s, %s, %s',
                self.userAgent,
                headers,
                e,
            )
            raise


class AppRunner:
    '''From aiohttp
    '''

    def __init__(
        self,
        host,
        port,
        remoteUrl
    ):
        self.host = host
        self.port = port
        self.remoteUrl = remoteUrl

    async def cleanup(self):
        pass

    async def setup(self, stop=None, block=False):
        '''It would be good to unify better unittest mode versus command mode,
           and get rid of block
        '''
        handler = functools.partial(
            msgHandler, remoteUrl=self.remoteUrl
        )

        if block:
            async with websockets.serve(
                handler,
                self.host,
                self.port,
                create_protocol=ServerProtocol
            ) as self.server:
                await stop
                self.closeRedis()
                await self.cleanup()
        else:
            self.server = await websockets.serve(
                handler,
                self.host,
                self.port,
                create_protocol=ServerProtocol
            )

    def run(self, stop):
        asyncio.get_event_loop().run_until_complete(self.setup(stop, block=True))

    async def closeServer(self):
        '''Used by the unittest'''
        # Now close websocket server
        self.server.close()
        await self.server.wait_closed()

    def terminate(self):
        '''Used by the unittest'''
        asyncio.get_event_loop().run_until_complete(self.cleanup())
        asyncio.get_event_loop().run_until_complete(self.closeServer())
