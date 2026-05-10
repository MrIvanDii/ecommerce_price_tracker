import pandas as pd
from src.config import BEST_PRICES_OUTPUT_PATH

df = pd.read_csv(BEST_PRICES_OUTPUT_PATH)
print(df.columns.tolist())
print(df.to_string())