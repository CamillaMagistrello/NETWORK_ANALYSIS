import networkx as nx
from pathlib import Path
import community as community_louvain
import time
import csv

BASE_DIR = Path(__file__).resolve().parent
G = nx.read_gexf(BASE_DIR.parent.parent / "data" / "anime_network.gexf")
RESULTS = BASE_DIR.parent.parent / "results" / "assignment1"

print("====================")
print("LOUVAIN ANALYSIS")
print("====================")


start = time.time()
partition = community_louvain.best_partition(G)
end = time.time()

print("Time:")
print(end-start)

number_communities = len(set(partition.values()))
print("Number of communities:")
print(number_communities)

sizes = {}
for node, community in partition.items():
    sizes[community] = sizes.get(community,0)+1

print("\nLargest communities:")
for c,s in sorted(sizes.items(), key=lambda x:x[1], reverse=True)[:10]:
    print(c,s)

with open(RESULTS/"louvain.csv","w",newline="",encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["node","community"])

    for node, community in partition.items():
        writer.writerow([node,community])

print("\nSaved")