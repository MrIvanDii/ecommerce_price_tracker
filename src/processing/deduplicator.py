from typing import List, Dict


def deduplicate_by_product_url(records: List[Dict]) -> List[Dict]:
    unique_records = {}

    for record in records:
        product_url = record.get("product_url")

        if not product_url:
            continue

        unique_records[product_url] = record

    return list(unique_records.values())