from src.sources import UKBULLION_LISTING_URLS
from src.scraper.ukbullion_parser import parse_ukbullion_listing


SOURCES = [
    {
        "name": "ukbullion",
        "listing_urls": UKBULLION_LISTING_URLS,
        "parser": parse_ukbullion_listing,
    }
]