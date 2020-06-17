import types
import asyncio
import selectors
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from aiohttp import ClientSession

import requests

from http_parser import HTTPRequest

SCHEME='http'
BASE_RESPONSE = 'HTTP/1.1 {} {}\n'


def accept_wrapper(sock, sel):
    conn, addr = sock.accept()
    print('[ACCEPT]', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def get_request_data(recv_data):
    request = HTTPRequest(recv_data)
    headers = request.get_headers()
    request_url = f'{SCHEME}://172.18.0.2{request.path}'

    content_length = headers.get('Content-Length', 0)
    request_body = request.get_body() 

    return {
            'headers': headers,
            'url': request_url,
            'data': request_body,
            'method': request.command,
        }


async def service_connection(key, mask, sel):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            try:
                request_data = get_request_data(recv_data)
                status, reason, headers, content = await fetch_response(**request_data)
                response = prepare_response(status, reason, headers, content)
                data.outb = response.encode('utf-8')
                
            except Exception as e:
                print(e)

        else:
            print('[CLOSE]', data.addr)
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


async def fetch_response(headers, url, data, method):
    async with ClientSession() as session:
        async with getattr(session, method.lower())(url) as response:
            headers = response.headers
            content = await response.read()

    return (response.status, response.reason, dict(headers), content)


def prepare_response(status, reason, headers, content):
    content = content.decode('utf-8')
    response_headers = BASE_RESPONSE.format(status, reason)
    for k, v in headers.items():
        if k in ['Content-Encoding', 'Transfer-Encoding']:
            continue
        response_headers += f'{k}:{v}\n'

    response_headers += f'Content-Length: {len(content)}\n'

    response = f'{response_headers}\n{content}'
    return response
