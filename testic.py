import pandas as pd
from src.config import LATEST_OUTPUT_PATH

df = pd.read_csv(LATEST_OUTPUT_PATH)
ukb = df[df["dealer"] == "ukbullion"]
print(ukb["availability"].value_counts())