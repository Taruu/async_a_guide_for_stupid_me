import time
# The concurrent.futures module provides a high-level interface for asynchronously executing callables.
from concurrent.futures import ThreadPoolExecutor as Executor


def worker(data):
    print(data ** 100)


start = time.time()
worker(9)
print(time.time() - start, end="\n\n")

start = time.time()
with Executor(max_workers=10) as exe:
    future = exe.submit(worker, 9)
print(time.time() - start)

"""
265613988875874769338781322035779626829233452653394495974574961739092490901302182994384699044001
1.8596649169921875e-05

265613988875874769338781322035779626829233452653394495974574961739092490901302182994384699044001
0.0003955364227294922
"""
