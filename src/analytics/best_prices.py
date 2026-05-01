from typing import List, Dict, Tuple


def get_group_key(record: Dict) -> Tuple:
    return (
        record.get("coin_family"),
        record.get("weight"),
    )


def find_best_prices(records: List[Dict]) -> List[Dict]:
    best_by_group = {}

    for record in records:
        price = record.get("price")
        coin_family = record.get("coin_family")
        weight = record.get("weight")

        if price is None:
            continue

        if not coin_family or not weight:
            continue

        group_key = get_group_key(record)

        if group_key not in best_by_group:
            best_by_group[group_key] = record
            continue

        current_best = best_by_group[group_key]

        if price < current_best.get("price"):
            best_by_group[group_key] = record

    return list(best_by_group.values())