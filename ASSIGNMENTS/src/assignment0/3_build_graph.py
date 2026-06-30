import pandas as pd
import networkx as nx
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT = BASE_DIR / "data" / "anime_filtered.csv"
OUTPUT = BASE_DIR / "data" / "anime_network.gexf"

df = pd.read_csv(INPUT)

print("Loaded anime:", len(df))
G = nx.Graph()

for _, row in df.iterrows():
    G.add_node(
        str(row["mal_id"]),
        title=row["title"],
        score=row["score"],
        members=row["members"]
    )
print("Nodes created:", G.number_of_nodes())

for i in range(len(df)):
    anime1 = df.iloc[i]
    genres1 = set(str(anime1["genres"]).split("|"))
    for j in range(i + 1, len(df)):
        anime2 = df.iloc[j]
        genres2 = set(str(anime2["genres"]).split("|"))
        common_genres = genres1.intersection(genres2)
        if len(common_genres) >= 2:
            G.add_edge(
                str(anime1["mal_id"]),
                str(anime2["mal_id"]),
                weight=len(common_genres)
            )

print("====================")
print("GRAPH CREATED")
print("====================")

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

nx.write_gexf(G, OUTPUT)

print("Saved:")
print(OUTPUT)