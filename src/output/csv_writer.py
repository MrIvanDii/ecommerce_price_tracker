import csv
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger("gold_coin_price_tracker")

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


def _check_unknown_fields(records: List[Dict]) -> None:
    known = set(FIELDNAMES)
    unknown = set()

    for record in records:
        for key in record.keys():
            if key not in known:
                unknown.add(key)

    if unknown:
        logger.warning(f"Unknown fields detected (will be ignored): {sorted(unknown)}")


def write_records_to_csv(records: List[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _check_unknown_fields(records)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def append_records_to_csv(records: List[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _check_unknown_fields(records)

    existing_records = []
    if output_path.exists():
        with open(output_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            existing_records = list(reader)

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
            retained_records.append(record)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(retained_records)
        writer.writerows(records)