from celery import Celery
import time

app = Celery("tasks", broker="redis://redis:6379/0")


@app.task
def run_heavy_celery_task():
    with open("/tmp/celery_test.txt", "wb") as f:
        f.write(b"x" * 100_000_000)
    time.sleep(2)
