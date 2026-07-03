import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import random
import csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

GRAPH = BASE_DIR / "data" / "anime_network.gexf"
RESULTS = BASE_DIR / "results" / "assignment0"
RESULTS.mkdir(parents=True, exist_ok=True)

G = nx.read_gexf(GRAPH)

# ====================
# NETWORK METRICS
# ====================

nodes = G.number_of_nodes()
edges = G.number_of_edges()

density = nx.density(G)
average_degree = sum(dict(G.degree()).values()) / nodes
clustering = nx.average_clustering(G)
assortativity = nx.degree_assortativity_coefficient(G)
components = nx.number_connected_components(G)

# Degree centrality
degree = nx.degree_centrality(G)

top_nodes = sorted(
    degree.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

# ====================
# LARGEST COMPONENT
# ====================

largest = max(nx.connected_components(G), key=len)
H = G.subgraph(largest)

# Diameter
diameter = nx.diameter(H)

# Faster average shortest path estimate
sample_size = min(50, H.number_of_nodes())
sample = random.sample(list(H.nodes()), sample_size)

paths = []
for node in sample:
    lengths = nx.single_source_shortest_path_length(H, node)
    paths.extend(lengths.values())

average_path = sum(paths) / len(paths)

# ====================
# SAVE METRICS
# ====================

REPORT = RESULTS / "4_analyze_graph.txt"

with open(REPORT, "w", encoding="utf-8") as file:

    def write(text=""):
        print(text)
        file.write(str(text) + "\n")

    write("====================")
    write("NETWORK INFO")
    write("====================")

    write(f"Nodes: {nodes}")
    write(f"Edges: {edges}")
    write(f"Density: {density:.6f}")
    write(f"Average degree: {average_degree:.2f}")
    write(f"Average clustering: {clustering:.6f}")
    write(f"Assortativity: {assortativity:.6f}")
    write(f"Connected components: {components}")
    write(f"Diameter: {diameter}")
    write(f"Average path length (estimated): {average_path:.6f}")

    write("")
    write("====================")
    write("TOP DEGREE CENTRALITY")
    write("====================")

    centrality_rows = []

    for node, value in top_nodes:
        title = G.nodes[node]["title"]
        write(f"{title}: {value:.6f}")
        centrality_rows.append([title, value])

# ====================
# SAVE CENTRALITY CSV
# ====================

with open(RESULTS / "centrality.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Anime", "Degree Centrality"])
    writer.writerows(centrality_rows)

# ====================
# DEGREE DISTRIBUTION
# ====================

degrees = [d for _, d in G.degree()]

plt.figure(figsize=(8, 5))
plt.hist(degrees, bins=50, edgecolor="black")

plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.title("Degree Distribution")

plt.tight_layout()
plt.savefig(RESULTS / "degree_distribution.png", dpi=300)

plt.close()

print("\nResults saved in:")
print(RESULTS)