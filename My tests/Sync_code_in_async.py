import time
import asyncio

class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration

def sync_sleep(sleep: float):
    time.sleep(sleep)
    return f"sync_task_result {time.time()}"


async def async_to_sync_driver():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, sync_sleep, (10))  # Making futures and banging on hold
    return result


async def async_sleep(sleep: float):
    await asyncio.sleep(sleep)
    return f"async_task_result {time.time()}"


async def main():
    sync_list_task = []
    async_list_task = []
    loop = asyncio.get_running_loop()
    while True:
        while len(sync_list_task) < 10:
            new_task = loop.create_task(async_to_sync_driver())
            sync_list_task.append(new_task)
        else:
            async for task in AsyncIterator(sync_list_task):
                if task.done():
                    print("sync_done!", task.result())
                    sync_list_task.remove(task)
        while len(async_list_task) < 10:
            new_task = loop.create_task(async_sleep(5))
            async_list_task.append(new_task)
        else:
            async for task in AsyncIterator(async_list_task):
                if task.done():
                    print("async_done!", task.result())
                    async_list_task.remove(task)
        # If we do not sleep in while then we will steal the entire loop and it will be blocked
        await asyncio.sleep(1)


asyncio.run(main())
