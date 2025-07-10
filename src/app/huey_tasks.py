from huey import RedisHuey
import time

huey = RedisHuey("my_app", host="redis", port=6379)


@huey.task()
def run_heavy_huey_task():
    with open("/tmp/huey_test.txt", "wb") as f:
        f.write(b"x" * 100_000_000)
    time.sleep(2)
