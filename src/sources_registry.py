from src.sources import UKBULLION_LISTING_URLS, BULLIONBYPOST_LISTING_URLS

from src.scraper.fetcher import fetch_html
from src.scraper.browser_fetcher import fetch_html_with_browser

from src.scraper.ukbullion_parser import parse_ukbullion_listing
from src.scraper.bullionbypost_parser import parse_bullionbypost_listing


SOURCES = [
    {
        "name": "UKBullion",
        "dealer": "ukbullion",
        "fetch_mode": "http",
        "listing_urls": UKBULLION_LISTING_URLS,
        "fetcher": fetch_html,
        "parser": parse_ukbullion_listing,
    },
    {
        "name": "BullionByPost",
        "dealer": "bullionbypost",
        "fetch_mode": "browser",
        "listing_urls": BULLIONBYPOST_LISTING_URLS,
        "fetcher": fetch_html_with_browser,
        "parser": parse_bullionbypost_listing,
    },
]