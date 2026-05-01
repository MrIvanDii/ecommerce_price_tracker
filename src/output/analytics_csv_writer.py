import csv
from pathlib import Path
from typing import List, Dict


PRICE_SPREAD_FIELDNAMES = [
    "coin_family",
    "weight",
    "min_price",
    "max_price",
    "spread_value",
    "spread_percent",
    "cheapest_dealer",
    "cheapest_product_name",
    "cheapest_product_url",
    "most_expensive_dealer",
    "most_expensive_product_name",
    "most_expensive_product_url",
    "records_compared",
]


def write_price_spreads_to_csv(records: List[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=PRICE_SPREAD_FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)