import os
from src.config import LOG_PATH

# Размер текущего лога
size = os.path.getsize(LOG_PATH)
print(f"app.log size: {size / 1024:.1f} KB")

# Проверяем наличие ротированных файлов
log_dir = LOG_PATH.parent
for f in sorted(log_dir.iterdir()):
    if "app.log" in f.name:
        print(f"{f.name}: {f.stat().st_size / 1024:.1f} KB")