import re
from typing import Optional, Dict


def extract_year(product_name: str) -> Optional[str]:
    match = re.search(r"\b(20\d{2}|19\d{2})\b", product_name)
    if not match:
        return None

    return match.group(1)


def extract_weight(product_name: str) -> Optional[str]:
    text = product_name.lower()

    weight_patterns = [
        (r"\b1\s*oz\b", "1oz"),
        (r"\b1/2\s*oz\b", "1/2oz"),
        (r"\b1\s*2oz\b", "1/2oz"),
        (r"\bhalf\s*ounce\b", "1/2oz"),
        (r"\b1/4\s*oz\b", "1/4oz"),
        (r"\b1\s*4oz\b", "1/4oz"),
        (r"\bquarter\s*ounce\b", "1/4oz"),
        (r"\b1/10\s*oz\b", "1/10oz"),
        (r"\btenth\s*ounce\b", "1/10oz"),
    ]

    for pattern, normalized_value in weight_patterns:
        if re.search(pattern, text):
            return normalized_value

    return None


def extract_coin_family(product_name: str) -> Optional[str]:
    text = product_name.lower()

    families = {
        "britannia": "britannia",
        "krugerrand": "krugerrand",
        "sovereign": "sovereign",
        "maple": "maple_leaf",
        "maple leaf": "maple_leaf",
        "eagle": "eagle",
        "kangaroo": "kangaroo",
        "panda": "panda",
        "philharmonic": "philharmonic",
    }

    for keyword, normalized_value in families.items():
        if keyword in text:
            return normalized_value

    return None


def extract_product_metadata(product_name: Optional[str]) -> Dict[str, Optional[str]]:
    if not product_name:
        return {
            "year": None,
            "weight": None,
            "coin_family": None,
        }

    return {
        "year": extract_year(product_name),
        "weight": extract_weight(product_name),
        "coin_family": extract_coin_family(product_name),
    }