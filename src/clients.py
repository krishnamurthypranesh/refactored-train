import time
import asyncio

import requests
from aiohttp import ClientSession

URL = 'http://localhost:5000/'

async def fetch_stuff(url, i):
    async with ClientSession() as session:
        async with session.get(url) as response:
            print('Here')
            start = time.time()
            response = await response.read()
            print('It\'s {} and response after: {} seconds'.format(
                i, time.time() - start))
            print(len(response))
        return response

loop = asyncio.get_event_loop()

tasks = []
for i in range(1):
    task = asyncio.ensure_future(fetch_stuff(URL, i))
    tasks.append(task)

start = time.time()
loop.run_until_complete(asyncio.wait(tasks))
end  = time.time()
print('Async: {}'.format(end - start))
