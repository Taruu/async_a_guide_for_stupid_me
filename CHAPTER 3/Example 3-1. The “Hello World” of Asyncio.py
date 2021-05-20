import asyncio
import time


async def main():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")


asyncio.run(main())

"""
Thu May 20 16:42:39 2021 Hello!
Thu May 20 16:42:40 2021 Goodbye!
"""
