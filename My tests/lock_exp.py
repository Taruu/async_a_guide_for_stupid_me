import asyncio
import aiohttp
from time import perf_counter

urls = ['https://readmanga.live/sitemap.xml',
        'http://api.nekos.fun:8080/api/neko',
        'https://randomfox.ca/',
        'https://readmanga.live/sitemap.xml',
        ] * 10

cache = {}

coro_lock = asyncio.Lock()


async def cache_get(url):
    global cache

    while coro_lock.locked():
        await asyncio.sleep(0)
    if url in cache:
        print(f"get from cache {url}")
        return cache.get(url)
    else:
        await coro_lock.acquire()
        print(f"get from internet {url}")
    async with aiohttp.ClientSession() as session:
        result = await session.get(url)
        content = await result.text()
        cache[url] = content
        coro_lock.release()
        return content


async def main():
    time_start = perf_counter()
    list_coros = [cache_get(url) for url in urls]
    await asyncio.gather(*list_coros)
    exec_time = perf_counter() - time_start
    print(f"Execution time: {exec_time} seconds")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
