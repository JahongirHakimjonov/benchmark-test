import asyncio
import time

import requests
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

redis_url = "redis://redis:6379"

result_backend = RedisAsyncResultBackend(redis_url=redis_url)
broker = RedisStreamBroker(url=redis_url).with_result_backend(result_backend)


@broker.task
async def taskiq_cpu_bound_task():
    count = 0
    for i in range(10**7):
        count += i
    return count


@broker.task
async def taskiq_io_bound_task():
    await asyncio.sleep(1)
    return "io_done"


@broker.task
async def taskiq_network_io_task():
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, requests.get, "https://httpbin.org/delay/1"
    )
    return response.status_code


@broker.task
async def taskiq_ram_heavy_task(size_mb: int = 500):
    size = size_mb * 1024 * 1024 // 8
    data = [0.0] * size
    await asyncio.sleep(5)
    return f"Allocated {size_mb}MB RAM"


@broker.task
async def taskiq_disk_heavy_task(size_mb: int = 500):
    path = f"/tmp/taskiq_disk_test_{time.time()}.bin"
    with open(path, "wb") as f:
        f.write(b"x" * size_mb * 1024 * 1024)
    await asyncio.sleep(2)
    return f"Wrote {size_mb}MB to disk: {path}"
