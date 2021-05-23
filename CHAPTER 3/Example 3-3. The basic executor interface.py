import asyncio
import time


async def main():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")


def blocking():
    time.sleep(0.5)
    print(f"{time.ctime()} Hello from a thread!")


loop = asyncio.get_event_loop()
task = loop.create_task(main())

loop.run_in_executor(None, blocking)
loop.run_until_complete(task)  # Run until the end of execution

pending = asyncio.all_tasks(loop=loop)  # get all tasks!! not return a Future
for task in pending:
    task.cancel()
group = asyncio.gather(*pending, return_exceptions=True)  # get "list" task to done in main loop
loop.run_until_complete(group)
loop.close()

"""
Thu May 20 19:49:13 2021 Hello!
Thu May 20 19:49:14 2021 Hello from a thread!
Thu May 20 19:49:14 2021 Goodbye!
"""
