import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATASET_PATH = BASE_DIR / "data" / "anime_info.csv"
RESULTS_DIR = BASE_DIR / "results" / "assignment0"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT = RESULTS_DIR / "1_explore_dataset.txt"

df = pd.read_csv(DATASET_PATH)

with open(OUTPUT, "w", encoding="utf-8") as f:

    def write(text=""):
        print(text)
        f.write(str(text) + "\n")

    write("\n" + "=" * 50)
    write("DATASET SHAPE")
    write("=" * 50)

    write(f"Rows: {df.shape[0]}")
    write(f"Columns: {df.shape[1]}")

    write("\n" + "=" * 50)
    write("COLUMNS")
    write("=" * 50)

    for col in df.columns:
        write(col)

    write("\n" + "=" * 50)
    write("MISSING VALUES")
    write("=" * 50)

    missing = df.isnull().sum().sort_values(ascending=False)
    write(missing[missing > 0].to_string())

    write("\n" + "=" * 50)
    write("SAMPLE ANIME")
    write("=" * 50)

    sample = df[
        [
            "title",
            "genres",
            "themes",
            "demographics",
            "score",
            "members",
        ]
    ].head(10)

    write(sample.to_string())

    write("\n" + "=" * 50)
    write("TYPE DISTRIBUTION")
    write("=" * 50)

    write(df["type"].value_counts().to_string())

    write("\n" + "=" * 50)
    write("DEMOGRAPHICS")
    write("=" * 50)

    write(df["demographics"].value_counts(dropna=False).to_string())

    write("\n" + "=" * 50)
    write("TOP 20 BY MEMBERS")
    write("=" * 50)

    top_members = (
        df[["title", "members"]]
        .sort_values("members", ascending=False)
        .head(20)
    )

    write(top_members.to_string(index=False))

    write("\n" + "=" * 50)
    write("TOP 20 BY SCORE")
    write("=" * 50)

    top_score = (
        df[df["score"].notna()][["title", "score"]]
        .sort_values("score", ascending=False)
        .head(20)
    )

    write(top_score.to_string(index=False))

    write("\n" + "=" * 50)
    write("MOST COMMON GENRES")
    write("=" * 50)

    genre_counter = {}
    for genres in df["genres"].dropna():
        for genre in str(genres).split("|"):
            genre = genre.strip()
            if genre:
                genre_counter[genre] = genre_counter.get(genre, 0) + 1

    genre_df = (
        pd.DataFrame(genre_counter.items(), columns=["genre", "count"])
        .sort_values("count", ascending=False)
    )

    write(genre_df.head(20).to_string(index=False))

    write("\n" + "=" * 50)
    write("MOST COMMON THEMES")
    write("=" * 50)

    theme_counter = {}
    for themes in df["themes"].dropna():
        for theme in str(themes).split("|"):
            theme = theme.strip()
            if theme:
                theme_counter[theme] = theme_counter.get(theme, 0) + 1

    theme_df = (
        pd.DataFrame(theme_counter.items(), columns=["theme", "count"])
        .sort_values("count", ascending=False)
    )
    write(theme_df.head(20).to_string(index=False))
    write("\nDataset exploration completed.")
print(f"\nResults saved to:\n{OUTPUT}")