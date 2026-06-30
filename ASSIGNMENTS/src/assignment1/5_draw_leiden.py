import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent
G = nx.read_gexf(BASE_DIR.parent.parent / "data" / "anime_network.gexf")
G = nx.relabel_nodes(G, lambda x: str(x))
RESULTS = BASE_DIR.parent.parent / "results" / "assignment1"

print("====================")
print("DRAW COMMUNITIES")
print("====================")

communities = {}
with open(RESULTS / "leiden.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        communities[str(row["node"])] = int(row["community"])
sizes = {}
for node, community in communities.items():
    sizes[community] = sizes.get(community, 0) + 1

largest_communities = sorted(
    sizes,
    key=sizes.get,
    reverse=True
)[:3]

print("Largest communities:")
for c in largest_communities:
    print(c, sizes[c])

nodes = [
    node
    for node in G.nodes()
    if node in communities
    and communities[node] in largest_communities
]

H = G.subgraph(nodes)
print("\nNodes drawn:", H.number_of_nodes())
print("Edges drawn:", H.number_of_edges())

colors = [
    communities[node]
    for node in H.nodes()
]
print("\nComputing layout...")
pos = nx.spring_layout(H, seed=42, k=0.05, iterations=50)
plt.figure(figsize=(12,12))
nx.draw_networkx_nodes(H, pos, node_color=colors, node_size=20)
nx.draw_networkx_edges(H, pos, alpha=0.05)

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