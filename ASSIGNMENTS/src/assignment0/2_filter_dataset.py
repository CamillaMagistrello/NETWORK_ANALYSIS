import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT = BASE_DIR / "data" / "anime_info.csv"
OUTPUT = BASE_DIR / "data" / "anime_filtered.csv"

RESULTS = BASE_DIR / "results" / "assignment0"
RESULTS.mkdir(parents=True, exist_ok=True)

REPORT = RESULTS / "2_filter_dataset.txt"

df = pd.read_csv(INPUT)
df = pd.read_csv(INPUT)

filtered = df[
    (df["members"] >= 50000)
    & (df["genres"].notna())
]

filtered = filtered.drop_duplicates(subset="mal_id")

print(f"Original anime: {len(df)}")
print(f"Filtered anime: {len(filtered)}")

filtered.to_csv(OUTPUT, index=False)

with open(REPORT, "w", encoding="utf-8") as f:
    f.write("DATASET FILTERING\n")
    f.write("=================\n")
    f.write(f"Original anime: {len(df)}\n")
    f.write(f"Filtered anime: {len(filtered)}\n")
    f.write(f"Removed anime: {len(df) - len(filtered)}\n")
    f.write("\nFiltering criteria:\n")
    f.write("- members >= 50000\n")
    f.write("- genres not null\n")

print(f"Saved filtered dataset to: {OUTPUT}")
print(f"Filtering summary saved to: {REPORT}")