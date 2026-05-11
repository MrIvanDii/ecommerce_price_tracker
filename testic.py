
import pandas as pd
from src.config import HISTORY_OUTPUT_PATH

df = pd.read_csv(HISTORY_OUTPUT_PATH)
print(f"Total rows: {len(df)}")
print(f"Date range: {df['timestamp'].min()} → {df['timestamp'].max()}")
print(f"Unique dates: {df['timestamp'].str[:10].nunique()}")
print(df['timestamp'].str[:10].value_counts().sort_index())
