from pathlib import Path
from dotenv import load_dotenv
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)

LOG_PATH = PROJECT_ROOT / "logs" / "app.log"

LATEST_OUTPUT_PATH = PROJECT_ROOT / "data" / "output" / "latest_prices.csv"
HISTORY_OUTPUT_PATH = PROJECT_ROOT / "data" / "output" / "price_history.csv"
BEST_PRICES_OUTPUT_PATH = PROJECT_ROOT / "data" / "output" / "best_prices.csv"
PRICE_SPREAD_OUTPUT_PATH = PROJECT_ROOT / "data" / "output" / "price_spread.csv"

REQUEST_DELAY_SECONDS = int(os.getenv("REQUEST_DELAY_SECONDS", 1))
RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3))
TIMEOUT = int(os.getenv("TIMEOUT", 20))
HISTORY_RETENTION_DAYS = int(os.getenv("HISTORY_RETENTION_DAYS", 90))

# Database
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "gold_tracker")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")