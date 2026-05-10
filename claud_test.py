# check_results.py — положи в корень проекта и запусти после main.py
import pandas as pd
from src.config import LATEST_OUTPUT_PATH, BEST_PRICES_OUTPUT_PATH, LOG_PATH

df = pd.read_csv(LATEST_OUTPUT_PATH)

# --- Общая картина ---
print("=== TOTAL RECORDS ===")
print(df.groupby(["dealer", "scrape_status"]).size().to_string())

# --- Atkinsons отдельно ---
atk = df[df["dealer"] == "atkinsons"]
print(f"\n=== ATKINSONS: {len(atk)} records ===")
print(atk[["product_name", "price", "weight", "price_per_oz", "availability", "scrape_status"]].to_string())

# --- Мусор / проблемы ---
print("\n=== ISSUES ===")
print("Missing price:    ", atk["price"].isna().sum())
print("Missing weight:   ", atk["weight"].isna().sum())
print("Missing p/oz:     ", atk["price_per_oz"].isna().sum())
print("Out of stock:     ", (atk["availability"] == "out_of_stock").sum())
print("Failed records:   ", (atk["scrape_status"] == "failed").sum())

failed = atk[atk["scrape_status"] == "failed"]
if not failed.empty:
    print("\n--- Failed records ---")
    print(failed[["product_name", "error_message"]].to_string())

# --- Последние строки лога ---
print("\n=== LAST 20 LOG LINES ===")
with open(LOG_PATH) as f:
    lines = f.readlines()
    print("".join(lines[-20:]))