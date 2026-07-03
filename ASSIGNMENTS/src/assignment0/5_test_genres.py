import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = BASE_DIR / "data" / "anime_filtered.csv"
RESULTS = BASE_DIR / "results" / "assignment0"
RESULTS.mkdir(parents=True, exist_ok=True)
OUTPUT = RESULTS / "5_test_genres.txt"
df = pd.read_csv(DATASET_PATH)

with open(OUTPUT, "w", encoding="utf-8") as file:
    def write(text=""):
        print(text)
        file.write(str(text) + "\n")

    write("====================")
    write("GENRE STATISTICS")
    write("====================")

    write(f"Anime: {len(df)}")

    write("")
    write("Unique genre combinations:")
    write(df["genres"].nunique())

    genre_counts = {}
    for genres in df["genres"].dropna():
        genre_set = genres.split("|")
        genre_counts[len(genre_set)] = (genre_counts.get(len(genre_set), 0) + 1)

    write("")
    write("Genres per anime:")

    for k in sorted(genre_counts):
        write(f"{k} genres -> {genre_counts[k]} anime")

print(f"\nResults saved to:\n{OUTPUT}")