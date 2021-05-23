import inspect


async def f():
    return 123


def g():
    yield 123


print(type(f), inspect.iscoroutinefunction(f))
print(type(g), inspect.iscoroutinefunction(g))

gen = g()

print(type(gen), inspect.iscoroutinefunction(gen))

coro = f()

print(type(coro), inspect.iscoroutinefunction(coro))
