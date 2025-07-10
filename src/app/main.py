from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

from app.celery_tasks import run_heavy_celery_task
from app.huey_tasks import run_heavy_huey_task
from app.taskiq_tasks import run_heavy_taskiq_task

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
    run_heavy_huey_task()
    return {"message": "Huey task triggered"}


@app.post("/celery-task")
async def celery_task():
    TASK_COUNTER.labels(type="celery").inc()
    run_heavy_celery_task.delay()
    return {"message": "Celery task triggered"}


@app.post("/taskiq-task")
async def taskiq_task():
    TASK_COUNTER.labels(type="taskiq").inc()
    # await broker.startup()
    await run_heavy_taskiq_task.kiq()
    # await broker.shutdown()
    return {"message": "Taskiq task triggered"}
