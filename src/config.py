from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

LOG_PATH = PROJECT_ROOT / "logs" / "app.log"

LATEST_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "output" / "latest_prices.csv"
)

HISTORY_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "output" / "price_history.csv"
)

BEST_PRICES_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "output" / "best_prices.csv"
)

PRICE_SPREAD_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "output" / "price_spread.csv"
)

REQUEST_DELAY_SECONDS = 1