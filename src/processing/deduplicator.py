from typing import List, Dict


def deduplicate_by_product_url(records: List[Dict]) -> List[Dict]:
    seen = {}

    for record in records:
        product_url = record.get("product_url")
        dealer = record.get("dealer", "")
        product_name_clean = record.get("product_name_clean", "") or ""

        # Основной ключ — URL
        # Фоллбэк — dealer + название (для UKBullion с разными URL одного товара)
        url_slug = product_url.rstrip("/").split("/")[-1] if product_url else None
        fallback_key = f"{dealer}::{product_name_clean.lower().strip()}"
        primary_key = f"{dealer}::{url_slug}" if url_slug else fallback_key

        if primary_key not in seen:
            seen[primary_key] = record

    return list(seen.values())