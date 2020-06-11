import socket
import selectors

from helpers import accept_wrapper, service_connection

HOST = '127.0.0.1'
PORT = 5000
sel = selectors.DefaultSelector()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()

print('Listening on', (HOST, PORT))

lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj, sel)
        else:
            service_connection(key, mask, sel)
