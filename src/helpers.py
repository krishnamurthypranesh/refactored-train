import types
import selectors

def accept_wrapper(sock, sel):
    conn, addr = sock.accept()
    print('Accept connection from ', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask, sel):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print('Closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print('Echoing', repr(data.outb), 'to', data.addr)
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
