import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent
G = nx.read_gexf(BASE_DIR.parent.parent / "data" / "anime_network.gexf")
RESULTS = BASE_DIR.parent.parent / "results" / "assignment1"

# Carica Louvain
partition = {}
with open(RESULTS / "louvain.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        partition[row["node"]] = int(row["community"])

# layout
print("Computing layout...")
pos = nx.spring_layout(G, seed=42)
colors = [
    partition[node]
    for node in G.nodes()
]

print("Drawing...")
plt.figure(figsize=(12,12))
nx.draw_networkx_nodes(
    G,
    pos,
    node_color=colors,
    node_size=10
)
nx.draw_networkx_edges(
    G,
    pos,
    alpha=0.1
)
plt.axis("off")
plt.savefig(
    RESULTS / "louvain_communities.png",
    dpi=300,
    bbox_inches="tight"
)

print("Saved:")
print(RESULTS / "louvain_communities.png")