import time

from src.config import (
    LOG_PATH,
    LATEST_OUTPUT_PATH,
    PRICE_SPREAD_OUTPUT_PATH,
    HISTORY_OUTPUT_PATH,
    BEST_PRICES_OUTPUT_PATH,
    REQUEST_DELAY_SECONDS,
)

from src.analytics.best_prices import find_best_prices
from src.analytics.price_spread import calculate_price_spreads
from src.output.analytics_csv_writer import write_price_spreads_to_csv

from src.logger import setup_logger
from src.sources_registry import SOURCES
from src.processing.deduplicator import deduplicate_by_product_url
from src.processing.validator import validate_records
from src.output.csv_writer import write_records_to_csv, append_records_to_csv
from src.output.google_sheets import (
    write_latest_prices,
    append_price_history,
    write_best_prices,
)


def main() -> None:
    logger = setup_logger(LOG_PATH)

    logger.info("Pipeline started")

    all_records = []

    total_sources = len(SOURCES)
    total_pages = 0
    successful_pages = 0
    empty_pages = 0
    failed_pages = 0

    for source in SOURCES:
        source_name = source["name"]
        dealer = source["dealer"]
        fetch_mode = source["fetch_mode"]
        listing_urls = source["listing_urls"]
        fetcher = source["fetcher"]
        parser = source["parser"]

        logger.info(
            f"Processing source: {source_name} | dealer={dealer} | fetch_mode={fetch_mode}"
        )

        for listing_url in listing_urls:
            total_pages += 1
            logger.info(f"Processing listing page: {listing_url}")

            try:
                html = fetcher(listing_url)
                records = parser(html, listing_url)

                if records:
                    successful_pages += 1
                    logger.info(f"Records found: {len(records)}")
                    all_records.extend(records)
                else:
                    empty_pages += 1
                    logger.warning(
                        f"No records found for listing page: {listing_url}"
                    )

            except Exception as exc:
                failed_pages += 1
                logger.error(
                    f"Failed to process listing page: {listing_url} | Error: {exc}"
                )

            finally:
                time.sleep(REQUEST_DELAY_SECONDS)

    unique_records = deduplicate_by_product_url(all_records)
    validated_records = validate_records(unique_records)
    best_price_records = find_best_prices(validated_records)

    price_spread_records = calculate_price_spreads(validated_records)
    write_records_to_csv(validated_records, LATEST_OUTPUT_PATH)
    write_price_spreads_to_csv(price_spread_records, PRICE_SPREAD_OUTPUT_PATH)
    append_records_to_csv(validated_records, HISTORY_OUTPUT_PATH)

    write_records_to_csv(best_price_records, BEST_PRICES_OUTPUT_PATH)
    logger.info(f"Best price records saved: {len(best_price_records)}")
    logger.info(f"Best prices CSV saved to: {BEST_PRICES_OUTPUT_PATH}")
    logger.info("Writing records to Google Sheets")
    write_latest_prices(validated_records)
    append_price_history(validated_records)
    write_best_prices(best_price_records)
    logger.info("Google Sheets updated successfully")

    success_count = sum(
        1 for r in validated_records if r.get("scrape_status") == "success"
    )
    partial_count = sum(
        1 for r in validated_records if r.get("scrape_status") == "partial"
    )
    failed_count = sum(
        1 for r in validated_records if r.get("scrape_status") == "failed"
    )

    logger.info("Pipeline summary")
    logger.info(f"Total sources: {total_sources}")
    logger.info(f"Total pages: {total_pages}")
    logger.info(f"Successful pages: {successful_pages}")
    logger.info(f"Empty pages: {empty_pages}")
    logger.info(f"Failed pages: {failed_pages}")
    logger.info(f"Total raw records parsed: {len(all_records)}")
    logger.info(f"Unique records saved: {len(validated_records)}")
    logger.info(f"Latest CSV saved to: {LATEST_OUTPUT_PATH}")
    logger.info(f"History CSV updated at: {HISTORY_OUTPUT_PATH}")
    logger.info(f"Price spread records saved: {len(price_spread_records)}")
    logger.info(f"Price spread CSV saved to: {PRICE_SPREAD_OUTPUT_PATH}")

    logger.info("Data quality summary")
    logger.info(f"Successful records: {success_count}")
    logger.info(f"Partial records: {partial_count}")
    logger.info(f"Failed records: {failed_count}")

    logger.info("Pipeline finished")


if __name__ == "__main__":
    main()