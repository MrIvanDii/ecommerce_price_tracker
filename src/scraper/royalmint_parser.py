# src/scraper/royalmint_parser.py
from datetime import datetime, timezone
from src.processing.product_metadata import (
    extract_product_metadata,
    normalize_product_name,
    calculate_price_per_oz,
)
from src.processing.cleaner import normalize_availability

from typing import Optional
import time
import requests
import logging
logger = logging.getLogger("gold_coin_price_tracker")

API_URL = "https://www.royalmint.com/search/GetProductListingJsonData"
BASE_URL = "https://www.royalmint.com"

CATALOG_ID = 1073743726  # Gold Coins
MAX_RESULTS = 9
DEALER = "royalmint"
SOURCE_CATEGORY = "Gold Coins"


def _build_payload(page: int) -> dict:
    return {
        "query": " ",
        "listingType": 1,
        "currentPage": page,
        "entrySortOrder": "NotSpecified",
        "FirstPageNumberOfResults": MAX_RESULTS,
        "HideOffsaleAndSoldOut": True,
        "HideOutOfStock": False,
        "cacheResultsForMinutes": 10,
        "catalogId": CATALOG_ID,
        "checkboxUrl": "/search/GetProductListingJsonData?q= &type=1&Sort_by=NotSpecified",  # ← добавить
        "maxResults": MAX_RESULTS,
        "mobileFullWidth": True,
    }


def _parse_item(item: dict) -> Optional[dict]:
    try:
        variant = item.get("VariantSchema", {})
        stock = item.get("StockSummary", {})

        product_name = item.get("DisplayName", "").strip()
        price = item.get("Price")
        currency = item.get("CurrencyCode", "GBP")
        entry_url = item.get("EntryUrl", "")
        availability_raw = stock.get("StatusMessage", "Unknown")

        if not product_name or price is None or not entry_url:
            return None

        product_url = BASE_URL + entry_url
        metadata = extract_product_metadata(product_name)
        product_name_clean = normalize_product_name(product_name)
        price_per_oz = calculate_price_per_oz(price, metadata["weight"])

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dealer": DEALER,
            "listing_url": product_url,
            "product_url": product_url,
            "source_category": SOURCE_CATEGORY,
            "product_name": product_name,
            "product_name_clean": product_name_clean,
            "year": metadata["year"],
            "weight": metadata["weight"],
            "coin_family": metadata["coin_family"],
            "price": float(price),
            "price_per_oz": price_per_oz,
            "currency": currency,
            "availability": normalize_availability(availability_raw),
            "raw_price_text": variant.get("Price", ""),
            "scrape_status": "success",
            "error_message": None,
        }
    except Exception as e:
        logger.warning(f"RoyalMint: failed to parse item: {e}")
        return None


def fetch_royalmint() -> list[dict]:
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
    })

    # Шаг 1: GET на листинг — получаем cookies и session
    try:
        session.get(
            "https://www.royalmint.com/invest/bullion/bullion-coins/gold-coins/",
            timeout=20,
        )
        logger.info("RoyalMint: session initialized")
    except Exception as e:
        logger.error(f"RoyalMint: session init failed: {e}")
        return []
    time.sleep(2)

    # Шаг 2: переключаем заголовки на JSON
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Referer": "https://www.royalmint.com/invest/bullion/bullion-coins/gold-coins/",
        "X-Requested-With": "XMLHttpRequest",
    })

    records = []

    try:
        resp = session.post(
            API_URL,
            json=_build_payload(1),
            params={"noCache": int(time.time() * 1000)},
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.error(f"RoyalMint: first request failed: {e}")
        return []

    total_pages = data.get("TotalPagesCount", 1)
    total_items = data.get("TotalItems", "?")
    logger.info(f"RoyalMint: {total_items} items across {total_pages} pages")

    for item in data.get("Items", []):
        record = _parse_item(item)
        if record:
            records.append(record)

    for page in range(2, total_pages + 1):
        time.sleep(1)
        try:
            resp = session.post(
                API_URL,
                json=_build_payload(page),
                params={"noCache": int(time.time() * 1000)},
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
            items = data.get("Items", [])
            for item in items:
                record = _parse_item(item)
                if record:
                    records.append(record)
            logger.info(f"RoyalMint: page {page}/{total_pages} — {len(items)} items")
        except Exception as e:
            logger.error(f"RoyalMint: page {page} failed: {e}")
            continue

    logger.info(f"RoyalMint: total parsed {len(records)} records")
    return records