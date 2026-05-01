from typing import List, Dict, Tuple


def get_group_key(record: Dict) -> Tuple:
    return (
        record.get("coin_family"),
        record.get("weight"),
    )


def should_exclude_from_price_spread(record: Dict) -> bool:
    product_name = (record.get("product_name_clean") or "").lower()

    excluded_keywords = [
        # Bulk products
        "tube",
        "pack",
        "lot",
        "bundle",
        "box of",

        # Premium / collectible / graded products
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


def calculate_price_spreads(records: List[Dict]) -> List[Dict]:
    grouped_records = {}

    for record in records:
        price = record.get("price")
        coin_family = record.get("coin_family")
        weight = record.get("weight")

        if price is None:
            continue

        if not coin_family or not weight:
            continue

        if should_exclude_from_price_spread(record):
            continue

        group_key = get_group_key(record)

        if group_key not in grouped_records:
            grouped_records[group_key] = []

        grouped_records[group_key].append(record)

    spread_results = []

    for group_key, group_records in grouped_records.items():
        if len(group_records) < 2:
            continue

        sorted_records = sorted(group_records, key=lambda r: r.get("price"))

        cheapest = sorted_records[0]
        most_expensive = sorted_records[-1]

        min_price = cheapest.get("price")
        max_price = most_expensive.get("price")

        spread_value = round(max_price - min_price, 2)

        spread_percent = None
        if min_price:
            spread_percent = round((spread_value / min_price) * 100, 2)

        spread_results.append(
            {
                "coin_family": group_key[0],
                "weight": group_key[1],
                "min_price": min_price,
                "max_price": max_price,
                "spread_value": spread_value,
                "spread_percent": spread_percent,
                "cheapest_dealer": cheapest.get("dealer"),
                "cheapest_product_name": cheapest.get("product_name_clean"),
                "cheapest_product_url": cheapest.get("product_url"),
                "most_expensive_dealer": most_expensive.get("dealer"),
                "most_expensive_product_name": most_expensive.get("product_name_clean"),
                "most_expensive_product_url": most_expensive.get("product_url"),
                "records_compared": len(group_records),
            }
        )

    return spread_results