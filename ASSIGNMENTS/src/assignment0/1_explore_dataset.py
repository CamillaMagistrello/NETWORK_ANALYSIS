import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = BASE_DIR / "data" / "anime_info.csv"
df = pd.read_csv(DATASET_PATH)

print("\n" + "=" * 50)
print("DATASET SHAPE")
print("=" * 50)

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\n" + "=" * 50)
print("COLUMNS")
print("=" * 50)

for col in df.columns:
    print(col)

print("\n" + "=" * 50)
print("MISSING VALUES")
print("=" * 50)

missing = df.isnull().sum().sort_values(ascending=False)
print(missing[missing > 0])

print("\n" + "=" * 50)
print("SAMPLE ANIME")
print("=" * 50)

print(
    df[
        [
            "title",
            "genres",
            "themes",
            "demographics",
            "score",
            "members",
        ]
    ].head(10)
)

print("\n" + "=" * 50)
print("TYPE DISTRIBUTION")
print("=" * 50)

print(df["type"].value_counts())

print("\n" + "=" * 50)
print("DEMOGRAPHICS")
print("=" * 50)

print(df["demographics"].value_counts(dropna=False))

print("\n" + "=" * 50)
print("TOP 20 BY MEMBERS")
print("=" * 50)

top_members = (
    df[["title", "members"]]
    .sort_values("members", ascending=False)
    .head(20)
)

print(top_members)

print("\n" + "=" * 50)
print("TOP 20 BY SCORE")
print("=" * 50)

top_score = (
    df[df["score"].notna()]
    [["title", "score"]]
    .sort_values("score", ascending=False)
    .head(20)
)

print(top_score)

print("\n" + "=" * 50)
print("MOST COMMON GENRES")
print("=" * 50)

genre_counter = {}
for genres in df["genres"].dropna():
    for genre in str(genres).split("|"):
        genre = genre.strip()
        if genre:
            genre_counter[genre] = genre_counter.get(genre, 0) + 1

genre_df = (pd.DataFrame(genre_counter.items(), columns=["genre", "count"]).sort_values("count", ascending=False))
print(genre_df.head(20))
print("\n" + "=" * 50)
print("MOST COMMON THEMES")
print("=" * 50)

theme_counter = {}
for themes in df["themes"].dropna():
    for theme in str(themes).split("|"):
        theme = theme.strip()
        if theme:
            theme_counter[theme] = theme_counter.get(theme, 0) + 1

theme_df = (pd.DataFrame(theme_counter.items(), columns=["theme", "count"]).sort_values("count", ascending=False))
print(theme_df.head(20))
print("\nDataset exploration completed.")