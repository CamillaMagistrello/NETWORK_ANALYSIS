import pandas as pd
import networkx as nx
from pathlib import Path
from collections import defaultdict

# -------------------------
# PATH SETUP
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

INPUT = BASE_DIR / "data" / "anime_filtered.csv"
OUTPUT = BASE_DIR / "data" / "anime_network.gexf"

RESULTS = BASE_DIR / "results" / "assignment0"
RESULTS.mkdir(parents=True, exist_ok=True)

REPORT = RESULTS / "3_build_graph.txt"

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv(INPUT)

print("Loaded anime:", len(df))

# -------------------------
# GRAPH INIT
# -------------------------
G = nx.Graph()

# -------------------------
# ADD NODES
# -------------------------
for _, row in df.iterrows():
    G.add_node(
        str(row["mal_id"]),
        title=row["title"],
        score=row["score"],
        members=row["members"]
    )

print("Nodes created:", G.number_of_nodes())

# -------------------------
# PREPROCESS GENRES
# -------------------------
df["genre_set"] = df["genres"].fillna("").apply(lambda x: set(x.split("|")))

# -------------------------
# BUILD GENRE INDEX (FAST)
# -------------------------
genre_map = defaultdict(list)

for _, row in df.iterrows():
    anime_id = str(row["mal_id"])
    for g in row["genre_set"]:
        if g:  # avoid empty strings
            genre_map[g].append(anime_id)

# -------------------------
# BUILD EDGES (NO O(N^2))
# -------------------------
for genre, anime_list in genre_map.items():
    for i in range(len(anime_list)):
        for j in range(i + 1, len(anime_list)):
            a = anime_list[i]
            b = anime_list[j]

            if G.has_edge(a, b):
                G[a][b]["weight"] += 1
            else:
                G.add_edge(a, b, weight=1)

# -------------------------
# STATS
# -------------------------
print("====================")
print("GRAPH CREATED")
print("====================")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# -------------------------
# SAVE GRAPH
# -------------------------
nx.write_gexf(G, OUTPUT)

# -------------------------
# REPORT
# -------------------------
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("GRAPH CONSTRUCTION\n")
    f.write("==================\n\n")

    f.write(f"Input anime: {len(df)}\n")
    f.write(f"Nodes: {G.number_of_nodes()}\n")
    f.write(f"Edges: {G.number_of_edges()}\n\n")

    f.write("Construction rule:\n")
    f.write("- One node = one anime\n")
    f.write("- Edge created if anime share at least 1 genre\n")
    f.write("- Weight = number of shared genres\n\n")

    f.write("Optimization:\n")
    f.write("- Replaced O(n^2) comparison with genre-based indexing\n")
    f.write("- Uses inverted index (genre → anime list)\n")

print(f"Graph saved to: {OUTPUT}")
print(f"Report saved to: {REPORT}")