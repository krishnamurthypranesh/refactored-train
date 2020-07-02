import time
import random
import socket
import asyncio
import selectors
import threading
from string import ascii_lowercase as a2z

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

def bootstrap(tasks):
    print(f'From bootstrap => Len tasks: {len(tasks)}')
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(*tasks)
    asyncio.gather(*tasks)

last_print = 0
MAX_THREADS = 4
processes = []

# this works
# extending this, is the new logic I'll use to code
# the entire server
# Algorithm:
# There are utmost n threads at any point of time
# Each thread can hold 5 tasks. Keep track of the tasks sent to each thread
# When a thread has 5 tasks, do not set tasks for it
# when a task in a thread finishes execution, decrement number of tasks in
#   thread by one. This thread is then available for use.
# use callbacks wrapped in functools.partial to make updates to the values of
# the task counters. use fut.add_done_callback(functools.partial()) to achieve
# this.

# multithreaded event loops seem to be failing. I think it's because of the
# global interpreter lock. A workaround is to use multiprocessing. Back to
# square one again. FCUK
loops = dict()
for i in range(MAX_THREADS):
    tid = ''.join([str(random.choice(list(a2z) + list(range(10))))
        for i in range(10)])
    loops[tid] = {'count': 0, 'loop': None}
    loop = asyncio.new_event_loop()
    thr = threading.Thread(target=loop.run_forever)
    thr.daemon = True
    thr.start()
    loops[tid]['loop'] = loop

print(loops)

task_count = 0
while True:
    events = sel.select(timeout=10)
    tasks = []
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj, sel)
        else:
            for k, v in loops.items():
                if v['count'] > 4:
                    continue
                else:
                    _loop = v['loop']
                    _loop_id = k
                    break
            fut = asyncio.run_coroutine_threadsafe(
                    service_connection(key, mask, sel), _loop)
            loops[k]['count'] += 1


    if time.time() - last_print > 10:
        print(f'Loop statuses: {loops}') 
        print('[ACTIVE CONNECTIONS] ', len(events))
        last_print = time.time()
