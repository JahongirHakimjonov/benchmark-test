from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

from app.celery_tasks import (
    celery_cpu_bound_task,
    celery_io_bound_task,
    celery_network_io_task,
    celery_ram_heavy_task,
    celery_disk_heavy_task,
)
from app.huey_tasks import (
    huey_cpu_bound_task,
    huey_io_bound_task,
    huey_network_io_task,
    huey_ram_heavy_task,
    huey_disk_heavy_task,
)
from app.taskiq_tasks import (
    taskiq_cpu_bound_task,
    taskiq_io_bound_task,
    taskiq_network_io_task,
    taskiq_ram_heavy_task,
    taskiq_disk_heavy_task,
)

app = FastAPI()

# Prometheus метрики
TASK_COUNTER = Counter(
    "background_tasks_total", "Count of triggered background tasks", ["type"]
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.post("/huey-task")
async def huey_task():
    TASK_COUNTER.labels(type="huey").inc()
    huey_cpu_bound_task()
    huey_io_bound_task()
    huey_network_io_task()
    huey_ram_heavy_task()
    huey_disk_heavy_task()
    return {"message": "Huey task triggered"}


@app.post("/celery-task")
async def celery_task():
    TASK_COUNTER.labels(type="celery").inc()
    celery_cpu_bound_task.delay()
    celery_io_bound_task.delay()
    celery_network_io_task.delay()
    celery_ram_heavy_task.delay()
    celery_disk_heavy_task.delay()
    return {"message": "Celery task triggered"}


@app.post("/taskiq-task")
async def taskiq_task():
    TASK_COUNTER.labels(type="taskiq").inc()
    await taskiq_cpu_bound_task.kiq()
    await taskiq_io_bound_task.kiq()
    await taskiq_network_io_task.kiq()
    await taskiq_ram_heavy_task.kiq()
    await taskiq_disk_heavy_task.kiq()
    return {"message": "Taskiq task triggered"}
