import time
import asyncio


def sync_sleep(sleep: float):
    time.sleep(sleep)
    return f"sync_task_result {time.time()}"


async def async_to_sync_driver():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, sync_sleep, (3))
    return result


async def async_sleep(sleep: float):
    await asyncio.sleep(sleep)
    return f"async_task_result {time.time()}"


async def main(sleep: float):
    sync_list_task = []
    async_list_task = []
    loop = asyncio.get_running_loop()
    while True:
        while len(sync_list_task) < 10:
            # print(time.ctime(), "async len task", len(sync_list_task))
            new_task = loop.create_task(async_to_sync_driver())
            sync_list_task.append(new_task)
        else:
            for task in sync_list_task:
                if task.done():
                    print("sync_done!", task.result())
                    sync_list_task.remove(task)
        while len(async_list_task) < 10:
            new_task = loop.create_task(async_sleep(2))
            async_list_task.append(new_task)
        else:
            for task in async_list_task:
                if task.done():
                    print("async_done!", task.result())
                    async_list_task.remove(task)
        await asyncio.sleep(1)


asyncio.run(main(0.1))
