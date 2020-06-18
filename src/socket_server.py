import time
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

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

worker_loop = asyncio.new_event_loop()
worker_thread = threading.Thread(target=start_loop, args=(worker_loop,))
worker_thread.start()

last_print = 0

while True:
    events = sel.select(timeout=10)
    loop = asyncio.get_event_loop()
    tasks = []
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj, sel)
        else:
            asyncio.run_coroutine_threadsafe(service_connection(key, mask,
                sel), worker_loop)

    if time.time() - last_print > 10:
        print('[ACTIVE CONNECTIONS] ', len(events))
        last_print = time.time()
