import asyncio

from aiohttp import ClientSession

URL = 'http://localhost:5000/'

async def fetch_stuff(url, i):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            print(f'It\'s {i}', len(response))

loop = asyncio.get_event_loop()

tasks = []
for i in range(50):
    task = asyncio.ensure_future(fetch_stuff(URL, i))
    tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))
