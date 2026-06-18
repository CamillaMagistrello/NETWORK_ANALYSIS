import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent
G = nx.read_gexf(BASE_DIR.parent.parent / "data" / "anime_network.gexf")
RESULTS = BASE_DIR.parent.parent / "results" / "assignment1"

communities = {}
with open(RESULTS / "leiden.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        communities[row["anime"]] = int(row["community"])

nodes = []
for node in G.nodes():
    if node in communities:
        nodes.append(node)

H = G.subgraph(nodes)

print("====================")
print("DRAW COMMUNITIES")
print("====================")

print("Nodes:", H.number_of_nodes())
print("Edges:", H.number_of_edges())

colors = []
for node in H.nodes():
    colors.append(communities[node])

pos = nx.spring_layout(H, seed=42)
plt.figure(figsize=(12,12))

nx.draw_networkx_nodes(
    H,
    pos,
    node_color=colors,
    node_size=10
)
nx.draw_networkx_edges(
    H,
    pos,
    alpha=0.05
)

plt.title("Anime network - Leiden communities")
plt.axis("off")
plt.savefig(
    RESULTS / "leiden_communities.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()
print("\nSaved:")
print(RESULTS / "leiden_communities.png")