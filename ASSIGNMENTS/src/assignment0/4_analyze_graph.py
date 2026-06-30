import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import random
import csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

G = nx.read_gexf(BASE_DIR / "data" / "anime_network.gexf")
RESULTS = BASE_DIR / "results" / "assignment0"
RESULTS.mkdir(exist_ok=True)

print("NETWORK INFO")
nodes = G.number_of_nodes()
edges = G.number_of_edges()
density = nx.density(G)
clustering = nx.average_clustering(G)
assortativity = nx.degree_assortativity_coefficient(G)
print("Nodes:", nodes)
print("Edges:", edges)
print("\nDensity:")
print(density)
print("\nAverage clustering:")
print(clustering)
print("\nAssortativity:")
print(assortativity)
print("\nTop degree centrality:")
degree = nx.degree_centrality(G)
top_nodes = []
for node, value in sorted(degree.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(G.nodes[node]["title"], value)
    top_nodes.append([G.nodes[node]["title"], value])
largest = max(nx.connected_components(G), key=len)
H = G.subgraph(largest)

print("\nDiameter:")
diameter = nx.diameter(H)
print(diameter)

print("\nAverage path length:")
sample = random.sample(list(H.nodes()), 300)
paths = []
for node in sample:
    distances = nx.single_source_shortest_path_length(H, node)
    paths.extend(distances.values())
average_path = sum(paths) / len(paths)
print(average_path)

# SAVE METRICS
with open(RESULTS / "metrics.txt", "w", encoding="utf-8") as file:

    file.write("====================\n")
    file.write("NETWORK INFO\n")
    file.write("====================\n")

    file.write(f"Nodes: {nodes}\n")
    file.write(f"Edges: {edges}\n")
    file.write(f"Density: {density}\n")
    file.write(f"Average clustering: {clustering}\n")
    file.write(f"Assortativity: {assortativity}\n")
    file.write(f"Average path length: {average_path}\n")
    file.write(f"Diameter: {diameter}\n")

# SAVE CENTRALITY
with open(RESULTS / "centrality.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["anime", "centrality"])
    for row in top_nodes:
        writer.writerow(row)

# SAVE GRAPH
degrees = [d for _, d in G.degree()]

plt.hist(degrees, bins=50)

plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.title("Degree distribution")
plt.savefig(RESULTS / "degree_distribution.png", dpi=300)

plt.close()
print("\nResults saved in:")
print(RESULTS)