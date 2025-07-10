import asyncio

from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

redis_url = "redis://redis:6379"

result_backend = RedisAsyncResultBackend(
    redis_url=redis_url,
)

broker = RedisStreamBroker(
    url=redis_url,
).with_result_backend(result_backend)


@broker.task
async def run_heavy_taskiq_task():
    with open("/tmp/taskiq_test.txt", "wb") as f:
        f.write(b"x" * 100_000_000)
    await asyncio.sleep(2)
