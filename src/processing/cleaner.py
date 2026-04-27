import re
from typing import Optional
from urllib.parse import urljoin


def clean_text(value: str) -> str:
    return " ".join(value.split()).strip()


def normalize_availability(raw_text: Optional[str]) -> str:
    if not raw_text:
        return "unknown"

    text = raw_text.strip().lower()

    if "out of stock" in text:
        return "out_of_stock"
    if "limited" in text:
        return "limited_stock"
    if "in stock" in text:
        return "in_stock"

    return "unknown"


def extract_price_from_text(raw_price_text: Optional[str]) -> Optional[float]:
    if not raw_price_text:
        return None

    match = re.search(r"£\s*([\d,]+(?:\.\d{2})?)", raw_price_text)
    if not match:
        return None

    numeric_part = match.group(1).replace(",", "")
    return float(numeric_part)


def detect_currency(raw_price_text: Optional[str]) -> Optional[str]:
    if not raw_price_text:
        return None

    if "£" in raw_price_text:
        return "GBP"

    return None


def make_absolute_url(base_url: str, product_url: str) -> str:
    return urljoin(base_url, product_url)