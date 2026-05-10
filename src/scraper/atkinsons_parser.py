from datetime import datetime, timezone
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from src.processing.cleaner import (
    clean_text,
    normalize_availability,
    make_absolute_url,
)
from src.processing.product_metadata import (
    extract_product_metadata,
    normalize_product_name,
    calculate_price_per_oz,
)
from src.processing.source_metadata import extract_source_category


DEALER = "atkinsons"
BASE_URL = "https://atkinsonsbullion.com"
LIVE_PRICING_URL = f"{BASE_URL}/api/livepricing"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Content-Type": "application/json",
    "Origin": BASE_URL,
    "Referer": BASE_URL,
}


def fetch_live_prices(sku_ids: List[str]) -> Dict[str, float]:
    if not sku_ids:
        return {}

    payload = {
        "basicProductIds": sku_ids,
        "fullProductIds": [],
        "sellProductIds": [],
    }

    try:
        response = requests.post(
            LIVE_PRICING_URL,
            json=payload,
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        prices = {}

        for item in data.get("basicProducts", []):
            sku_id = str(item.get("skuId", ""))
            raw_price = item.get("price")

            if not sku_id or raw_price is None:
                continue

            try:
                price = float(str(raw_price).replace(",", ""))
                prices[sku_id] = price
            except (ValueError, TypeError):
                continue

        return prices

    except Exception:
        return {}


def parse_atkinsons_listing(html: str, listing_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    source_category = extract_source_category(listing_url)

    cards_meta = extract_cards_metadata(soup)

    if not cards_meta:
        return []

    sku_ids = [card["sku_id"] for card in cards_meta]
    live_prices = fetch_live_prices(sku_ids)

    records = []
    timestamp = datetime.now(timezone.utc).isoformat()

    for card in cards_meta:
        try:
            record = build_record(
                card=card,
                live_prices=live_prices,
                listing_url=listing_url,
                source_category=source_category,
                timestamp=timestamp,
            )
            records.append(record)

        except Exception as exc:
            records.append(
                build_failed_record(
                    card=card,
                    listing_url=listing_url,
                    source_category=source_category,
                    timestamp=timestamp,
                    error_message=f"Card parsing error: {exc}",
                )
            )

    return records


def extract_cards_metadata(soup: BeautifulSoup) -> List[Dict]:
    cards_meta = []

    cards = soup.select("div.product-card")

    for card in cards:
        text_container = card.select_one("div.product-card__text-container")

        if not text_container:
            continue

        sku_id = text_container.get("data-prod")

        if not sku_id:
            continue

        title_tag = text_container.select_one("p.product-card__title a")

        if not title_tag:
            continue

        product_name = clean_text(title_tag.get_text(" ", strip=True))
        product_url = title_tag.get("href", "")

        if product_url:
            product_url = make_absolute_url(BASE_URL, product_url)

        card_text = clean_text(card.get_text(" ", strip=True)).lower()

        availability_raw = "In Stock"

        if "out of stock" in card_text or "sold out" in card_text:
            availability_raw = "Out of Stock"

        cards_meta.append(
            {
                "sku_id": str(sku_id),
                "product_name": product_name,
                "product_url": product_url,
                "availability_raw": availability_raw,
            }
        )

    return cards_meta


def build_record(
    card: Dict,
    live_prices: Dict[str, float],
    listing_url: str,
    source_category: str,
    timestamp: str,
) -> Dict:
    sku_id = card["sku_id"]
    product_name = card["product_name"]
    product_url = card["product_url"]
    availability_raw = card["availability_raw"]

    product_name_clean = normalize_product_name(product_name)
    metadata = extract_product_metadata(product_name_clean)

    price = live_prices.get(sku_id)
    price_per_oz = calculate_price_per_oz(price, metadata.get("weight"))

    currency = "GBP" if price is not None else None
    raw_price_text = f"£{price:,.2f}" if price is not None else None

    if price is not None and product_name and product_url:
        scrape_status = "success"
        error_message = None
    elif product_name and product_url:
        scrape_status = "partial"
        error_message = f"No live price returned for sku_id={sku_id}"
    else:
        scrape_status = "failed"
        error_message = "Missing product name or URL"

    return {
        "timestamp": timestamp,
        "dealer": DEALER,
        "listing_url": listing_url,
        "source_category": source_category,
        "product_name": product_name,
        "product_name_clean": product_name_clean,
        "year": metadata.get("year"),
        "weight": metadata.get("weight"),
        "coin_family": metadata.get("coin_family"),
        "product_url": product_url,
        "price": price,
        "price_per_oz": price_per_oz,
        "currency": currency,
        "availability": normalize_availability(availability_raw),
        "raw_price_text": raw_price_text,
        "scrape_status": scrape_status,
        "error_message": error_message,
    }


def build_failed_record(
    card: Optional[Dict],
    listing_url: str,
    source_category: str,
    timestamp: str,
    error_message: str,
) -> Dict:
    product_name = card.get("product_name") if card else None
    product_url = card.get("product_url") if card else None

    return {
        "timestamp": timestamp,
        "dealer": DEALER,
        "listing_url": listing_url,
        "source_category": source_category,
        "product_name": product_name,
        "product_name_clean": normalize_product_name(product_name) if product_name else None,
        "year": None,
        "weight": None,
        "coin_family": None,
        "product_url": product_url,
        "price": None,
        "price_per_oz": None,
        "currency": None,
        "availability": "unknown",
        "raw_price_text": None,
        "scrape_status": "failed",
        "error_message": error_message,
    }