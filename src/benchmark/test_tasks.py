import pytest
import requests

FASTAPI_URL = "http://fastapi-app:8000"


@pytest.mark.benchmark(group="tasks")
def test_huey_benchmark(benchmark):
    benchmark(lambda: requests.post(f"{FASTAPI_URL}/huey-task"))


@pytest.mark.benchmark(group="tasks")
def test_celery_benchmark(benchmark):
    benchmark(lambda: requests.post(f"{FASTAPI_URL}/celery-task"))


@pytest.mark.benchmark(group="tasks")
def test_taskiq_benchmark(benchmark):
    benchmark(lambda: requests.post(f"{FASTAPI_URL}/taskiq-task"))
