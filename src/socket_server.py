import socket
import asyncio
import selectors
import threading
from concurrent.futures import ThreadPoolExecutor

from helpers import accept_wrapper, service_connection


HOST = '127.0.0.1'
PORT = 5000
sel = selectors.DefaultSelector()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()

print('[LISTENING]', (HOST, PORT))

lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

i = 0
while True:
    events = sel.select(timeout=10)
    loop = asyncio.get_event_loop()
    tasks = []
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj, sel)
        else:
            tasks.append(service_connection(key, mask, sel))

    if len(tasks) > 0:
        loop.run_until_complete(asyncio.gather(*tasks))

    print('[ACTIVE CONNECTIONS] ', len(events))
    i += 1
