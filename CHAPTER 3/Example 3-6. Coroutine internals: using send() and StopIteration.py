async def f():
    return 123

coro = f()
try:
    coro.send(None)
except StopIteration as e:
    print("The answer was:", e.value)


"""
The answer was: 123
"""