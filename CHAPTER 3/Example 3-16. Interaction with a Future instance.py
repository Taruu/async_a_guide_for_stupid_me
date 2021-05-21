import asyncio


async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    f.set_result("I have finished")


loop = asyncio.get_event_loop()
fut = asyncio.Future()

print(fut.done())
print(loop.create_task(main(fut)))
print(loop.run_until_complete())
print(fut.done())
