import networkx as nx
from pathlib import Path
import community as community_louvain
import time
import csv

BASE_DIR = Path(__file__).resolve().parent
G = nx.read_gexf(BASE_DIR.parent.parent / "data" / "anime_network.gexf")
RESULTS = BASE_DIR.parent.parent / "results" / "assignment1"
RESULTS.mkdir(exist_ok=True)

print("====================")
print("LOUVAIN ANALYSIS")
print("====================")

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

print("\nRunning Louvain...")

start = time.time()
partition = community_louvain.best_partition(G)
end = time.time()

runtime = end - start

print("Time:")
print(runtime)

number_communities = len(set(partition.values()))

print("\nNumber of communities:")
print(number_communities)

sizes = {}

for node, community in partition.items():
    sizes[community] = sizes.get(community, 0) + 1

print("\nLargest communities:")

for community, size in sorted(sizes.items(), key=lambda x:x[1], reverse=True)[:10]:
    print(community, size)


# SAVE CSV
with open(RESULTS / "louvain.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "node",
        "anime",
        "community"
    ])
    for node, community in partition.items():
        writer.writerow([
            node,
            G.nodes[node]["title"],
            community
        ])

with open(RESULTS / "louvain_info.txt", "w", encoding="utf-8") as file:
    file.write("====================\n")
    file.write("LOUVAIN RESULTS\n")
    file.write("====================\n\n")

    file.write(f"Nodes: {G.number_of_nodes()}\n")
    file.write(f"Edges: {G.number_of_edges()}\n")
    file.write(f"Runtime: {runtime:.4f} s\n")
    file.write(f"Total communities: {number_communities}\n\n")

    file.write("Largest communities:\n")

    for community, size in sorted(sizes.items(), key=lambda x:x[1], reverse=True)[:10]:
        file.write(f"{community}: {size} nodes\n")

print("\nResults saved in:")
print(RESULTS)