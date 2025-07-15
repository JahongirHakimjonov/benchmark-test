import time

import requests
from celery import Celery

app = Celery("tasks", broker="redis://redis:6379/0")


@app.task
def celery_cpu_bound_task():
    count = 0
    for i in range(10**7):
        count += i
    return count


@app.task
def celery_io_bound_task():
    time.sleep(1)
    return "io_done"


@app.task
def celery_network_io_task():
    response = requests.get("https://httpbin.org/delay/1")
    return response.status_code


@app.task
def celery_ram_heavy_task(size_mb: int = 500):
    size = size_mb * 1024 * 1024 // 8
    data = [0.0] * size
    time.sleep(5)
    return f"Allocated {size_mb}MB RAM"


@app.task
def celery_disk_heavy_task(size_mb: int = 500):
    path = f"/tmp/celery_disk_test_{time.time()}.bin"
    with open(path, "wb") as f:
        f.write(b"x" * size_mb * 1024 * 1024)
    time.sleep(2)
    return f"Wrote {size_mb}MB to disk: {path}"
