from src.output.db import upsert_latest, insert_history, upsert_best
from src.logger import setup_logger
import src.config as config

logger = setup_logger(config.LOG_PATH)


def _prepare_record(record: dict) -> dict:
    """Extract only the fields needed for price_latest and price_history."""
    return {
        "timestamp": record.get("timestamp"),
        "dealer": record.get("dealer"),
        "product_name_clean": record.get("product_name_clean"),
        "coin_family": record.get("coin_family"),
        "year": record.get("year"),
        "weight": record.get("weight"),
        "price": record.get("price"),
        "price_per_oz": record.get("price_per_oz"),
        "currency": record.get("currency"),
        "availability": record.get("availability") == "in_stock",
        "listing_url": record.get("listing_url") or record.get("product_url"),
    }


def _prepare_best_record(record: dict) -> dict:
    """Extract only the fields needed for price_best."""
    return {
        "coin_family": record.get("coin_family"),
        "weight": record.get("weight"),
        "best_price": record.get("best_price"),
        "best_price_per_oz": record.get("best_price_per_oz"),
        "dealer": record.get("dealer"),
        "product_name_clean": record.get("product_name_clean"),
        "year": record.get("year"),
        "currency": record.get("currency"),
        "listing_url": record.get("listing_url") or record.get("product_url"),
    }


def write_to_db(latest: list[dict], history: list[dict], best: list[dict]):
    """Write all pipeline outputs to PostgreSQL."""

    logger.info("DB write started")

    try:
        prepared_latest = [_prepare_record(r) for r in latest]
        upsert_latest(prepared_latest)
    except Exception as e:
        logger.error(f"Failed to write price_latest: {e}")

    try:
        prepared_history = [_prepare_record(r) for r in history]
        insert_history(prepared_history, retention_days=config.HISTORY_RETENTION_DAYS)
    except Exception as e:
        logger.error(f"Failed to write price_history: {e}")

    try:
        prepared_best = [_prepare_best_record(r) for r in best]
        upsert_best(prepared_best)
    except Exception as e:
        logger.error(f"Failed to write price_best: {e}")

    logger.info("DB write completed")