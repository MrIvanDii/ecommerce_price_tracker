from pathlib import Path
from pprint import pprint

from src.scraper.fetcher import fetch_html
from src.scraper.ukbullion_parser import parse_ukbullion_listing
from src.output.csv_writer import write_records_to_csv, append_records_to_csv

from src.sources import UKBULLION_LISTING_URLS


def deduplicate_by_product_url(records: list[dict]) -> list[dict]:
    unique_records = {}

    for record in records:
        product_url = record.get("product_url")

        if not product_url:
            continue

        unique_records[product_url] = record

    return list(unique_records.values())


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent

    latest_output_path = (
        project_root / "data" / "output" / "ukbullion_latest_prices.csv"
    )

    history_output_path = (
        project_root / "data" / "output" / "ukbullion_price_history.csv"
    )

    all_records = []

    for listing_url in UKBULLION_LISTING_URLS:
        print(f"Processing listing page: {listing_url}")

        html = fetch_html(listing_url)
        records = parse_ukbullion_listing(html, listing_url)

        print(f"Records found: {len(records)}")
        all_records.extend(records)

    unique_records = deduplicate_by_product_url(all_records)

    write_records_to_csv(unique_records, latest_output_path)
    append_records_to_csv(unique_records, history_output_path)

    print()
    print(f"Total raw records parsed: {len(all_records)}")
    print(f"Unique records saved: {len(unique_records)}")
    print(f"Latest CSV saved to: {latest_output_path}")
    print(f"History CSV updated at: {history_output_path}")
    print()

    for record in unique_records[:5]:
        pprint(record)
        print("-" * 80)


if __name__ == "__main__":
    main()