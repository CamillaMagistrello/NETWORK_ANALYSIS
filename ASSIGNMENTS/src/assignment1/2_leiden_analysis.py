import networkx as nx
from pathlib import Path
import igraph as ig
import leidenalg
import time
import csv

BASE_DIR = Path(__file__).resolve().parent
G = nx.read_gexf(BASE_DIR.parent.parent / "data" / "anime_network.gexf")
RESULTS = BASE_DIR.parent.parent / "results" / "assignment1"
RESULTS.mkdir(exist_ok=True)

print("====================")
print("LEIDEN ANALYSIS")
print("====================")

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

print("\nRunning Leiden...")
nodes = list(G.nodes())

mapping = {}
for i, node in enumerate(nodes):
    mapping[node] = i
edges = []
for u, v in G.edges():
    edges.append((mapping[u], mapping[v]))
IG = ig.Graph(edges=edges)
IG.vs["name"] = nodes
start = time.time()
communities = leidenalg.find_partition(IG, leidenalg.ModularityVertexPartition)
end = time.time()

print("Time:")
print(end - start)

number_communities = len(communities)

print("\nNumber of communities:")
print(number_communities)

sizes = {}

for i, community in enumerate(communities):
    sizes[i] = len(community)

print("\nLargest communities:")

for community, size in sorted(sizes.items(), key=lambda x:x[1], reverse=True)[:10]:
    print(community, size)

with open(RESULTS / "leiden.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["node", "anime", "community"])
    for community_id, community in enumerate(communities):
        for node in community:
            writer.writerow([nodes[node], G.nodes[nodes[node]]["title"], community_id])

with open(RESULTS / "leiden_info.txt", "w", encoding="utf-8") as file:

    file.write("====================\n")
    file.write("LEIDEN RESULTS\n")
    file.write("====================\n\n")

    file.write(f"Nodes: {G.number_of_nodes()}\n")
    file.write(f"Edges: {G.number_of_edges()}\n")
    file.write(f"Total communities: {number_communities}\n\n")

    file.write("Largest communities:\n")

    for community, size in sorted(sizes.items(), key=lambda x:x[1], reverse=True)[:10]:
        file.write(f"{community}: {size} nodes\n")

print("\nResults saved in:")
print(RESULTS)