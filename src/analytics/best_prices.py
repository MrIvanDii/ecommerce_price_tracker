from typing import List, Dict, Tuple


def get_group_key(record: Dict) -> Tuple:
    return (
        record.get("coin_family"),
        record.get("weight"),
    )


def find_best_prices(records: List[Dict]) -> List[Dict]:
    grouped_records = {}

    for record in records:
        coin_family = record.get("coin_family")
        weight = record.get("weight")
        price_per_oz = record.get("price_per_oz")

        if not coin_family or not weight:
            continue

        if price_per_oz is None:
            continue

        if record.get("availability") == "out_of_stock":
            continue

        if should_exclude_from_best_prices(record):
            continue

        group_key = get_group_key(record)

        if group_key not in grouped_records:
            grouped_records[group_key] = []

        grouped_records[group_key].append(record)

    best_price_records = []

    for group_key, group_records in grouped_records.items():
        best_record = min(
            group_records,
            key=lambda r: r.get("price_per_oz"),
        )

        best_price_records.append(best_record)

    return best_price_records


def should_exclude_from_best_prices(record: Dict) -> bool:
    product_name = (record.get("product_name_clean") or "").lower()

    excluded_keywords = [
        "empty tube",
        "tube",
        "pack",
        "lot",
        "bundle",
        "box of",
        "proof",
        "ngc",
        "pcgs",
        "pf70",
        "pf69",
        "ms70",
        "ms69",
        "graded",
        "boxed",
        "gift boxed",
        "limited edition",
        "commemorative",
    ]

    return any(keyword in product_name for keyword in excluded_keywords)