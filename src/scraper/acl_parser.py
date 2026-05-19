from datetime import datetime, timezone
from typing import List, Dict, Optional

from bs4 import BeautifulSoup

from src.scraper.fetcher import fetch_html
from src.processing.source_metadata import extract_source_category
from src.processing.cleaner import (
    clean_text,
    normalize_availability,
    extract_price_from_text,
    detect_currency,
)
from src.processing.product_metadata import (
    extract_product_metadata,
    normalize_product_name,
    calculate_price_per_oz,
)

SKIP_URL_FRAGMENTS = [
    "/gold-service/",
    "/uncategorised/",
    "/subscription",
    "cookieyes.com",
    "box-of-",
]


def fetch_acl_product_urls(listing_url: str) -> List[str]:
    """
    Fetches category page and extracts unique product URLs.
    Used as pre_fetcher in sources_registry.
    """
    html = fetch_html(listing_url)
    soup = BeautifulSoup(html, "html.parser")

    seen = set()
    urls = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/product/" not in href:
            continue
        if not href.startswith("https://acl-uk.online"):
            continue
        if any(fragment in href for fragment in SKIP_URL_FRAGMENTS):
            continue
        if href not in seen:
            seen.add(href)
            urls.append(href)

    return urls


def parse_acl_product_page(html: str, listing_url: str) -> List[Dict]:
    """
    Parses a single ACL product page.
    Returns a list with one record (or empty list if filtered/failed).
    """
    soup = BeautifulSoup(html, "html.parser")

    # Название
    title_tag = soup.find("h1", class_="product_title")
    if not title_tag:
        return []
    product_name = clean_text(title_tag.get_text())

    # Фильтр серебра
    if "silver" in product_name.lower():
        return []

    # URL товара — берём из canonical
    canonical = soup.find("link", rel="canonical")
    product_url = canonical["href"] if canonical else listing_url

    # Цена
    price_tag = soup.find("p", class_="price")
    raw_price_text = clean_text(price_tag.get_text()) if price_tag else None
    price = extract_price_from_text(raw_price_text)
    currency = detect_currency(raw_price_text) if raw_price_text else "GBP"

    # Availability из классов корневого div
    root_div = soup.find("div", class_="product")
    if root_div:
        classes = root_div.get("class", [])
        if "outofstock" in classes:
            raw_availability = "Out Of Stock"
        elif "instock" in classes:
            raw_availability = "In Stock"
        else:
            raw_availability = None
    else:
        raw_availability = None

    # Метаданные
    metadata = extract_product_metadata(product_name)
    product_name_clean = normalize_product_name(product_name)
    price_per_oz = calculate_price_per_oz(price, metadata["weight"])
    source_category = extract_source_category(listing_url)

    # Статус
    if product_name and price is not None:
        scrape_status = "success"
        error_message = None
    elif product_name:
        scrape_status = "partial"
        error_message = "Price not found."
    else:
        scrape_status = "failed"
        error_message = "Could not extract product name."

    return [{
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dealer": "acl",
        "listing_url": listing_url,
        "source_category": source_category,
        "product_name": product_name,
        "product_name_clean": product_name_clean,
        "year": metadata["year"],
        "weight": metadata["weight"],
        "coin_family": metadata["coin_family"],
        "product_url": product_url,
        "price": price,
        "price_per_oz": price_per_oz,
        "currency": currency,
        "availability": normalize_availability(raw_availability),
        "raw_price_text": raw_price_text,
        "scrape_status": scrape_status,
        "error_message": error_message,
    }]