#!/usr/bin/env python3
import os
import json
from array import array

import asyncio
import aiohttp.web


# global variables
WEBHOST = os.getenv('WEBHOST', '0.0.0.0')
WEBPORT = int(os.getenv('WEBPORT', 8080))
UDPHOST = os.getenv('UDPHOST', '0.0.0.0')
UDPPORT = int(os.getenv('UDPPORT', 1234))

NUM_POINTS = 625

# array if uint16_t values
points = array('H')


class UdpServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        global points
        if len(data) != NUM_POINTS * 2:
            # invalid datagram size
            print(f'Received unknown data (expecting {NUM_POINTS * 2} bytes):')
            print(data)
        else:
            # updating NUM_POINTS array
            points = array('H')
            points.frombytes(data)


async def index(request):
    return aiohttp.web.FileResponse('static/index.html')


async def websocket_handler(request):
    global points
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready, waiting for configuration JSON message')

    cfg = await ws.receive_json()
    print('Received configuration: ', cfg)

    # now start sending points every interval seconds from configuration object
    while not ws.closed:
        await ws.send_json(list(points))
        await asyncio.sleep(cfg['interval'])

    print('Websocket connection closed')
    return ws


def main():
    # empty points array
    global points
    points = array('H')
    for i in range(NUM_POINTS):
        points.append(0)

    # prepare web application
    app = aiohttp.web.Application()
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/ws', websocket_handler)

    # prepare and start udp server
    loop = asyncio.get_event_loop()
    listen = loop.create_datagram_endpoint(UdpServerProtocol, local_addr=(UDPHOST, UDPPORT))
    loop.run_until_complete(listen)

    # start web application
    aiohttp.web.run_app(app, host=WEBHOST, port=WEBPORT)


if __name__ == '__main__':
    main()
