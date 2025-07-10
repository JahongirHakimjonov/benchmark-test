import json

import matplotlib.pyplot as plt

# Загрузка данных
with open("benchmarks/Linux-CPython-3.11-64bit/0001_results.json") as f:
    data = json.load(f)

# Подготовка
benchmarks = data["benchmarks"]
names = [b["name"] for b in benchmarks]
means = [b["stats"]["mean"] * 1000 for b in benchmarks]  # в миллисекундах
errs = [b["stats"]["stddev"] * 1000 for b in benchmarks]

# Построение
plt.figure(figsize=(8, 4))
plt.bar(names, means, yerr=errs, capsize=5)
plt.ylabel("Время выполнения, мс")
plt.title("Сравнение производительности Huey, Celery и Taskiq")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
