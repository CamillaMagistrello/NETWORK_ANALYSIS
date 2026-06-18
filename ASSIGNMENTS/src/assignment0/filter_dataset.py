import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INPUT = BASE_DIR.parent / "data" / "anime_info.csv"
OUTPUT = BASE_DIR.parent / "data" / "anime_filtered.csv"

df = pd.read_csv(INPUT)

filtered = df[
    (df["members"] >= 50000)
    & (df["genres"].notna())
]

print(f"Original anime: {len(df)}")
print(f"Filtered anime: {len(filtered)}")

filtered.to_csv(OUTPUT, index=False)

print(f"Saved to {OUTPUT}")