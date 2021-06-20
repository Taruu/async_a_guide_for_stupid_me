import asyncio
import aiohttp
from time import perf_counter

cache = {}
stuff_lock = asyncio.Lock()
SLOW_URL = 'https://readmanga.live/sitemap.xml'
urls = ['https://readmanga.live/sitemap.xml',
        'http://api.nekos.fun:8080/api/neko',
        'https://randomfox.ca/',
        'https://readmanga.live/sitemap.xml',
        ] * 10
async def make_cached_get_request(url, cache: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            stuff = await resp.text()
            cache[url] = stuff
            return stuff


# попробуйте снять lock с этой функции
# и увидете, что урл не попадёт в кеш
async def get_stuff(url):
    async with stuff_lock:
        global cache
        if url in cache:
            print(f"get from cache {url}")
            return cache[url]
        print(f"get from internet {url}")
        return await make_cached_get_request(url, cache)


async def parse_stuff(url):
    return await get_stuff(url)


async def use_stuff(url):
    return await get_stuff(url)


async def do_work():
    async with aiohttp.ClientSession() as session:
        async with session.get(SLOW_URL) as resp:
            out = await resp.text()
            return out


async def main():
    time_start = perf_counter()
    list_coro = [parse_stuff(url) for url in urls]
    list_coro.extend([use_stuff(url) for url in urls ])
    await asyncio.gather(
        *list_coro
    )
    exec_time = perf_counter() - time_start
    print(f"Execution time: {exec_time} seconds")


# тут я вынужденно использую ло
loop = asyncio.get_event_loop()
loop.run_until_complete(main())