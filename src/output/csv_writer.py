import csv
from pathlib import Path
from typing import List, Dict


FIELDNAMES = [
    "timestamp",
    "dealer",
    "listing_url",
    "product_name",
    "year",
    "weight",
    "coin_family",
    "product_url",
    "price",
    "currency",
    "availability",
    "raw_price_text",
    "scrape_status",
    "error_message",
]


def write_records_to_csv(records: List[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)


def append_records_to_csv(records: List[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = output_path.exists()

    with open(output_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        if not file_exists:
            writer.writeheader()

        writer.writerows(records)