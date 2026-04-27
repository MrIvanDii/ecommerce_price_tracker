from pprint import pprint

from src.scraper.fetcher import fetch_html
from src.scraper.ukbullion_parser import parse_ukbullion_listing


def main() -> None:
    listing_url = "https://www.ukbullion.com/gold/buy-gold-coins/popular-gold-coins.html"

    html = fetch_html(listing_url)
    records = parse_ukbullion_listing(html, listing_url)

    print(f"Total records parsed: {len(records)}")
    print()

    for record in records[:5]:
        pprint(record)
        print("-" * 80)


if __name__ == "__main__":
    main()