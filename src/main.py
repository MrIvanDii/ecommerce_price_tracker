from pprint import pprint
from typing import List, Dict

from src.config import LOG_PATH, LATEST_OUTPUT_PATH, HISTORY_OUTPUT_PATH
from src.logger import setup_logger
from src.sources import UKBULLION_LISTING_URLS
from src.scraper.fetcher import fetch_html
from src.scraper.ukbullion_parser import parse_ukbullion_listing
from src.output.csv_writer import write_records_to_csv, append_records_to_csv


def deduplicate_by_product_url(records: List[Dict]) -> List[Dict]:
    unique_records = {}

    for record in records:
        product_url = record.get("product_url")

        if not product_url:
            continue

        unique_records[product_url] = record

    return list(unique_records.values())


def main() -> None:
    logger = setup_logger(LOG_PATH)

    logger.info("Pipeline started")

    all_records = []

    for listing_url in UKBULLION_LISTING_URLS:
        logger.info(f"Processing listing page: {listing_url}")

        try:
            html = fetch_html(listing_url)
            records = parse_ukbullion_listing(html, listing_url)

            logger.info(f"Records found: {len(records)}")
            all_records.extend(records)

        except Exception as exc:
            logger.error(
                f"Failed to process listing page: {listing_url} | Error: {exc}"
            )

    unique_records = deduplicate_by_product_url(all_records)

    write_records_to_csv(unique_records, LATEST_OUTPUT_PATH)
    append_records_to_csv(unique_records, HISTORY_OUTPUT_PATH)

    logger.info(f"Total raw records parsed: {len(all_records)}")
    logger.info(f"Unique records saved: {len(unique_records)}")
    logger.info(f"Latest CSV saved to: {LATEST_OUTPUT_PATH}")
    logger.info(f"History CSV updated at: {HISTORY_OUTPUT_PATH}")
    logger.info("Pipeline finished")

    print()
    print("Sample records:")

    for record in unique_records[:5]:
        pprint(record)
        print("-" * 80)


if __name__ == "__main__":
    main()