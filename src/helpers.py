import types
import asyncio
import selectors
from concurrent.futures import ThreadPoolExecutor

import requests

from http_parser import HTTPRequest

SCHEME='http'
BASE_RESPONSE = 'HTTP/1.1 {} {}\n'

executor = ThreadPoolExecutor(2)

def accept_wrapper(sock, sel):
    conn, addr = sock.accept()
    print('[ACCEPT]', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

async def fetch_site_data(url, method, headers, body={}):
    loop = asyncio.get_event_loop()
    f = getattr(requests, method.lower())
    response = await loop.run_in_executor(executor, f, url, headers, body)
    return response

def service_connection(key, mask, sel):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            request = HTTPRequest(recv_data)
            headers = request.get_headers()
            request_url = f'{SCHEME}://172.18.0.2{request.path}'

            content_length = headers.get('Content-Length', 0)
            request_body = request.get_body() 

            site_response = getattr(requests, request.command.lower())(
                        url=request_url, headers=headers,
                        data=request_body,
                    )

            content = site_response.content.decode('utf-8')
            response_headers = BASE_RESPONSE.format(
                        site_response.status_code,
                        site_response.reason
                    )

            for k, v in site_response.headers.items():
                if k in ['Content-Encoding', 'Transfer-Encoding']:
                    continue
                response_headers += f'{k}:{v}\n'

            response_headers += f'Content-Length: {len(content)}\n'

            response = f'{response_headers}\n{content}'

            data.outb = response.encode('utf-8')

        else:
            print('[CLOSE]', data.addr)
            sel.unregister(sock)
            sock.close()

        if mask & selectors.EVENT_WRITE:
            if data.outb:
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
