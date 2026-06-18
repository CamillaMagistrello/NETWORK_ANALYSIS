import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR.parent / "data" / "anime_filtered.csv"

df = pd.read_csv(DATASET_PATH)

print("Anime:", len(df))

print("\nUnique genre combinations:")
print(df["genres"].nunique())

genre_counts = {}

for genres in df["genres"].dropna():
    genre_set = genres.split("|")

    genre_counts[len(genre_set)] = (
        genre_counts.get(len(genre_set), 0) + 1
    )

print("\nGenres per anime:")
for k in sorted(genre_counts):
    print(f"{k} genres -> {genre_counts[k]} anime")