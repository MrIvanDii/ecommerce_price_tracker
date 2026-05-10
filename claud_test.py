# claud_test.py
import pandas as pd
from src.config import LATEST_OUTPUT_PATH

df = pd.read_csv(LATEST_OUTPUT_PATH)

for dealer in df["dealer"].unique():
    d = df[df["dealer"] == dealer]
    print(f"\n=== {dealer.upper()} ({len(d)} records) ===")
    print(f"Missing weight:    {d['weight'].isna().sum()}")
    print(f"Missing price_per_oz: {d['price_per_oz'].isna().sum()}")
    print(f"Missing coin_family:  {d['coin_family'].isna().sum()}")

    # Показать записи с missing weight
    no_weight = d[d["weight"].isna()][["product_name", "price", "coin_family"]]
    if not no_weight.empty:
        print("\nMissing weight:")
        for _, row in no_weight.iterrows():
            print(f"  [{row['coin_family']}] {row['product_name']}")