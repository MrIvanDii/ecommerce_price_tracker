from datetime import datetime, timezone
import re
from typing import List, Dict, Optional

from bs4 import BeautifulSoup

from src.processing.cleaner import (
    clean_text,
    normalize_availability,
    extract_price_from_text,
    detect_currency,
    make_absolute_url,
)

from src.processing.product_metadata import (
    extract_product_metadata,
    normalize_product_name,
)


def parse_ukbullion_listing(html: str, listing_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")

    records = []

    more_info_links = soup.find_all(
        "a",
        string=lambda s: s and "More Info" in s
    )

    for link in more_info_links:
        try:
            record = parse_product_card_from_more_info_link(link, listing_url)
            if record:
                records.append(record)

        except Exception as exc:
            records.append(
                {
                    "dealer": "ukbullion",
                    "listing_url": listing_url,
                    "product_name": None,
                    "product_url": None,
                    "price": None,
                    "currency": None,
                    "availability": "unknown",
                    "raw_price_text": None,
                    "scrape_status": "failed",
                    "error_message": f"Card parsing error: {exc}",
                }
            )

    return records


def parse_product_card_from_more_info_link(link, listing_url: str) -> Optional[Dict]:
    card = link.find_parent(["li", "div", "article"])

    if card:
        parent_text = clean_text(card.get_text(" ", strip=True))
    else:
        parent_text = clean_text(link.parent.get_text(" ", strip=True))

    product_url = link.get("href")
    if not product_url:
        return None

    product_url = make_absolute_url(listing_url, product_url)

    product_name = extract_product_name_from_block(parent_text)

    if not product_name:
        product_name = extract_product_name_from_url(product_url)
        metadata = extract_product_metadata(product_name)
        product_name_clean = normalize_product_name(product_name)

    raw_price_text = extract_1_plus_price(parent_text)
    raw_availability = extract_availability(parent_text)

    price = extract_price_from_text(raw_price_text)
    currency = detect_currency(raw_price_text)

    if product_name and raw_price_text and price is not None:
        scrape_status = "success"
        error_message = None
    elif product_name and (raw_price_text or raw_availability):
        scrape_status = "partial"
        error_message = "Partial card extraction."
    else:
        scrape_status = "failed"
        error_message = "Could not extract core product fields."

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dealer": "ukbullion",
        "listing_url": listing_url,
        "product_name": product_name,
        "product_name_clean": product_name_clean,
        "year": metadata["year"],
        "weight": metadata["weight"],
        "coin_family": metadata["coin_family"],
        "product_url": product_url,
        "price": price,
        "currency": currency,
        "availability": normalize_availability(raw_availability),
        "raw_price_text": raw_price_text,
        "scrape_status": scrape_status,
        "error_message": error_message,
    }


def extract_product_name_from_block(block_text: str) -> Optional[str]:
    patterns = [
        r"^(.*?)\s+From Just",
        r"^(.*?)\s+Out Of Stock",
        r"^(.*?)\s+More Info",
    ]

    for pattern in patterns:
        match = re.search(pattern, block_text)
        if match:
            value = clean_text(match.group(1))
            return value or None

    return None


def extract_product_name_from_url(product_url: str) -> Optional[str]:
    slug = product_url.rstrip("/").split("/")[-1]
    slug = slug.replace(".html", "")
    slug = slug.replace("-", " ")
    return clean_text(slug).title()


def extract_1_plus_price(block_text: str) -> Optional[str]:
    match = re.search(r"1\+\s*£\s*[\d,]+(?:\.\d{2})?", block_text)
    if not match:
        return None

    return clean_text(match.group(0))


def extract_availability(block_text: str) -> Optional[str]:
    lower_text = block_text.lower()

    if "out of stock" in lower_text:
        return "Out Of Stock"

    if "in stock" in lower_text:
        return "In Stock"

    return None