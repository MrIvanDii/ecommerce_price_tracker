from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

LOG_PATH = PROJECT_ROOT / "logs" / "app.log"

LATEST_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "output" / "ukbullion_latest_prices.csv"
)

HISTORY_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "output" / "ukbullion_price_history.csv"
)