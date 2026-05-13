import mysql.connector
from mysql.connector import Error
import src.config as config
from src.logger import setup_logger

logger = setup_logger(config.LOG_PATH)


def get_connection():
    """Create and return a MySQL connection."""
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )


def upsert_latest(records: list[dict]):
    """Truncate and reload price_latest table."""
    if not records:
        logger.warning("upsert_latest: no records to insert")
        return

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE price_latest")

        sql = """
            INSERT INTO price_latest
                (timestamp, dealer, product_name_clean, coin_family,
                 year, weight, price, price_per_oz, currency,
                 availability, listing_url)
            VALUES
                (%(timestamp)s, %(dealer)s, %(product_name_clean)s,
                 %(coin_family)s, %(year)s, %(weight)s, %(price)s,
                 %(price_per_oz)s, %(currency)s, %(availability)s,
                 %(listing_url)s)
        """
        cursor.executemany(sql, records)
        conn.commit()
        logger.info(f"upsert_latest: inserted {cursor.rowcount} records")

    except Error as e:
        logger.error(f"upsert_latest failed: {e}")
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()


def insert_history(records: list[dict], retention_days: int = 90):
    """Append to price_history and delete records older than retention_days."""
    if not records:
        logger.warning("insert_history: no records to insert")
        return

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO price_history
                (timestamp, dealer, product_name_clean, coin_family,
                 year, weight, price, price_per_oz, currency,
                 availability, listing_url)
            VALUES
                (%(timestamp)s, %(dealer)s, %(product_name_clean)s,
                 %(coin_family)s, %(year)s, %(weight)s, %(price)s,
                 %(price_per_oz)s, %(currency)s, %(availability)s,
                 %(listing_url)s)
        """
        cursor.executemany(sql, records)

        cursor.execute("""
            DELETE FROM price_history
            WHERE created_at < NOW() - INTERVAL %s DAY
        """, (retention_days,))

        conn.commit()
        logger.info(f"insert_history: inserted {len(records)} records, "
                    f"deleted old records beyond {retention_days} days")

    except Error as e:
        logger.error(f"insert_history failed: {e}")
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()


def upsert_best(records: list[dict]):
    """Truncate and reload price_best table."""
    if not records:
        logger.warning("upsert_best: no records to insert")
        return

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE price_best")

        sql = """
            INSERT INTO price_best
                (coin_family, weight, best_price, best_price_per_oz,
                 dealer, product_name_clean, year, currency, listing_url)
            VALUES
                (%(coin_family)s, %(weight)s, %(best_price)s,
                 %(best_price_per_oz)s, %(dealer)s, %(product_name_clean)s,
                 %(year)s, %(currency)s, %(listing_url)s)
        """
        cursor.executemany(sql, records)
        conn.commit()
        logger.info(f"upsert_best: inserted {cursor.rowcount} records")

    except Error as e:
        logger.error(f"upsert_best failed: {e}")
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()