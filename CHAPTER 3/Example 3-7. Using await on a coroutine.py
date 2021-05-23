
async def f():
    #await asyncio.sleep(1.0)
    return 123


async def main():
    result = await f()
    return result

coro = main()
try:
    coro.send(None)
except StopIteration as e:
    print("The answer was:", e.value)
