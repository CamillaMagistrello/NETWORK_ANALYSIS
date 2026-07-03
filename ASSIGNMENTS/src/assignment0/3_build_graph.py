import pandas as pd
import networkx as nx
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT = BASE_DIR / "data" / "anime_filtered.csv"
OUTPUT = BASE_DIR / "data" / "anime_network.gexf"
RESULTS = BASE_DIR / "results" / "assignment0"
RESULTS.mkdir(parents=True, exist_ok=True)
REPORT = RESULTS / "3_build_graph.txt"
df = pd.read_csv(INPUT)

print("Loaded anime:", len(df))
G = nx.Graph()

for _, row in df.iterrows():
    G.add_node(str(row["mal_id"]), title=row["title"], score=row["score"], members=row["members"])

print("Nodes created:", G.number_of_nodes())

df["genre_set"] = df["genres"].apply(lambda x: set(x.split("|")))

for i in range(len(df)):
    anime1 = df.iloc[i]
    genres1 = anime1["genre_set"]

    for j in range(i + 1, len(df)):
        anime2 = df.iloc[j]
        genres2 = anime2["genre_set"]

        common = genres1 & genres2
        n_common = len(common)

        if n_common >= 2:
            G.add_edge(str(anime1["mal_id"]), str(anime2["mal_id"]), weight=n_common)

print("====================")
print("GRAPH CREATED")
print("====================")

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

nx.write_gexf(G, OUTPUT)

with open(REPORT, "w", encoding="utf-8") as f:
    f.write("GRAPH CONSTRUCTION\n")
    f.write("==================\n")
    f.write(f"Input anime: {len(df)}\n")
    f.write(f"Nodes: {G.number_of_nodes()}\n")
    f.write(f"Edges: {G.number_of_edges()}\n")
    f.write("\nConstruction rule:\n")
    f.write("- One node represents one anime.\n")
    f.write("- An edge is created if two anime share at least 2 genres.\n")
    f.write("- Edge weight = number of shared genres.\n")

print(f"Graph saved to: {OUTPUT}")
print(f"Construction summary saved to: {REPORT}")