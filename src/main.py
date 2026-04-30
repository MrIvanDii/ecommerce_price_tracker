import time
from pprint import pprint

from src.config import (
    LOG_PATH,
    LATEST_OUTPUT_PATH,
    HISTORY_OUTPUT_PATH,
    REQUEST_DELAY_SECONDS,
)
from src.logger import setup_logger
from src.sources import UKBULLION_LISTING_URLS
from src.scraper.fetcher import fetch_html
from src.scraper.ukbullion_parser import parse_ukbullion_listing
from src.processing.deduplicator import deduplicate_by_product_url
from src.output.csv_writer import write_records_to_csv, append_records_to_csv
from src.output.google_sheets import write_latest_prices, append_price_history
from src.processing.validator import validate_records


def main() -> None:
    logger = setup_logger(LOG_PATH)

    logger.info("Pipeline started")

    all_records = []

    total_pages = len(UKBULLION_LISTING_URLS)
    successful_pages = 0
    empty_pages = 0
    failed_pages = 0

    for listing_url in UKBULLION_LISTING_URLS:
        logger.info(f"Processing listing page: {listing_url}")

        try:
            html = fetch_html(listing_url)
            records = parse_ukbullion_listing(html, listing_url)

            if records:
                successful_pages += 1
                logger.info(f"Records found: {len(records)}")
                all_records.extend(records)
            else:
                empty_pages += 1
                logger.warning(f"No records found for listing page: {listing_url}")

        except Exception as exc:
            failed_pages += 1
            logger.error(
                f"Failed to process listing page: {listing_url} | Error: {exc}"
            )

        finally:
            time.sleep(REQUEST_DELAY_SECONDS)

    unique_records = deduplicate_by_product_url(all_records)

    validated_records = validate_records(unique_records)

    write_records_to_csv(validated_records, LATEST_OUTPUT_PATH)
    append_records_to_csv(validated_records, HISTORY_OUTPUT_PATH)

    logger.info("Writing records to Google Sheets")
    write_latest_prices(validated_records)
    append_price_history(validated_records)
    logger.info("Google Sheets updated successfully")

    logger.info("Pipeline summary")
    logger.info(f"Total pages: {total_pages}")
    logger.info(f"Successful pages: {successful_pages}")
    logger.info(f"Empty pages: {empty_pages}")
    logger.info(f"Failed pages: {failed_pages}")
    logger.info(f"Total raw records parsed: {len(all_records)}")
    logger.info(f"Unique records saved: {len(validated_records)}")
    logger.info(f"Latest CSV saved to: {LATEST_OUTPUT_PATH}")
    logger.info(f"History CSV updated at: {HISTORY_OUTPUT_PATH}")
    logger.info("Pipeline finished")

    print()
    print("Sample records:")

    for record in validated_records[:5]:
        pprint(record)
        print("-" * 80)


if __name__ == "__main__":
    main()