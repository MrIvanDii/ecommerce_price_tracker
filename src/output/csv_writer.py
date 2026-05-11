import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict


FIELDNAMES = [
    "timestamp",
    "dealer",
    "listing_url",
    "source_category",
    "product_name",
    "product_name_clean",
    "year",
    "weight",
    "coin_family",
    "product_url",
    "price",
    "price_per_oz",
    "currency",
    "availability",
    "raw_price_text",
    "scrape_status",
    "error_message",
]

HISTORY_RETENTION_DAYS = 90


def write_records_to_csv(records: List[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)


def append_records_to_csv(records: List[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # --- Читаем существующую историю ---
    existing_records = []
    if output_path.exists():
        with open(output_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            existing_records = list(reader)

    # --- Отсекаем записи старше 90 дней ---
    cutoff = datetime.now(timezone.utc) - timedelta(days=HISTORY_RETENTION_DAYS)
    retained_records = []

    for record in existing_records:
        timestamp_str = record.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(timestamp_str)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if ts >= cutoff:
                retained_records.append(record)
        except (ValueError, TypeError):
            # Если timestamp не парсится — оставляем запись
            retained_records.append(record)

    # --- Пишем retained + новые записи ---
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(retained_records)
        writer.writerows(records)