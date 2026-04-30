import re
from datetime import datetime, timezone
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
from src.processing.source_metadata import extract_source_category


def parse_product_card(card, listing_url: str) -> Optional[Dict]:
    card_text = clean_text(card.get_text(" ", strip=True))

    link = card.select_one("a[href]")
    if not link:
        return None

    product_url = make_absolute_url(listing_url, link.get("href"))

    product_name = extract_product_name_from_block(card_text)

    if not product_name or product_name.lower() in ["in stock", "awaiting stock", "out of stock"]:
        product_name = extract_product_name_from_url(product_url)

    product_name_clean = normalize_product_name(product_name)
    metadata = extract_product_metadata(product_name_clean)

    raw_price_text = extract_from_price(card_text)
    raw_availability = extract_availability(card_text)

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
        "dealer": "bullionbypost",
        "listing_url": listing_url,
        "source_category": extract_source_category(listing_url),
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


def parse_bullionbypost_listing(html: str, listing_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    records = []

    product_cards = soup.select("div.card.product-module")

    for card in product_cards:
        try:
            record = parse_product_card(card, listing_url)

            if record:
                records.append(record)

        except Exception as exc:
            records.append(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "dealer": "bullionbypost",
                    "listing_url": listing_url,
                    "source_category": extract_source_category(listing_url),
                    "product_name": None,
                    "product_name_clean": None,
                    "year": None,
                    "weight": None,
                    "coin_family": None,
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


def parse_product_card_from_buy_link(link, listing_url: str) -> Optional[Dict]:
    card = link.find_parent(["li", "div", "article", "tr"])

    if card:
        card_text = clean_text(card.get_text(" ", strip=True))
    else:
        card_text = clean_text(link.parent.get_text(" ", strip=True))

    product_url = link.get("href")

    if not product_url:
        return None

    product_url = make_absolute_url(listing_url, product_url)

    product_name = extract_product_name_from_block(card_text)

    if not product_name or product_name.lower() in ["in stock", "awaiting stock", "out of stock"]:
        product_name = extract_product_name_from_url(product_url)

    product_name_clean = normalize_product_name(product_name)
    metadata = extract_product_metadata(product_name_clean)

    raw_price_text = extract_from_price(card_text)
    raw_availability = extract_availability(card_text)

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
        "dealer": "bullionbypost",
        "listing_url": listing_url,
        "source_category": extract_source_category(listing_url),
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
        r"^(.*?)\s+In Stock",
        r"^(.*?)\s+Awaiting Stock",
        r"^(.*?)\s+from £",
        r"^(.*?)\s+Buy",
    ]

    for pattern in patterns:
        match = re.search(pattern, block_text, flags=re.IGNORECASE)

        if match:
            value = clean_text(match.group(1))
            return value or None

    return None


def extract_product_name_from_url(product_url: str) -> Optional[str]:
    slug = product_url.rstrip("/").split("/")[-1]
    slug = slug.replace("-", " ")

    replacements = {
        "1oz": "1oz",
        "2026": "2026",
        "2025": "2025",
        "britannia": "Britannia",
        "gold": "Gold",
        "coin": "Coin",
        "coins": "Coins",
        "tube": "Tube",
        "one ounce": "1oz",
    }

    name = clean_text(slug).title()

    name = name.replace("1Oz", "1oz")
    name = name.replace("Britannia", "Britannia")
    name = name.replace("Gold", "Gold")
    name = name.replace("Coin", "Coin")

    return name


def extract_from_price(block_text: str) -> Optional[str]:
    match = re.search(r"from\s+£\s*[\d,]+(?:\.\d{2})?", block_text, flags=re.IGNORECASE)

    if not match:
        return None

    return clean_text(match.group(0))


def extract_availability(block_text: str) -> Optional[str]:
    lower_text = block_text.lower()

    if "in stock" in lower_text:
        return "In Stock"

    if "awaiting stock" in lower_text:
        return "Out of Stock"

    if "out of stock" in lower_text:
        return "Out of Stock"

    return None