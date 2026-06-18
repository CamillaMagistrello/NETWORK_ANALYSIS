import networkx as nx
import pickle
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
G = nx.read_gexf(BASE_DIR.parent.parent / "data" / "anime_network.gexf")

print("====================")
print("GRAPH ANALYSIS")
print("====================")

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# Diameter
if nx.is_connected(G):
    diameter = nx.approximation.diameter(G)
else:
    largest_cc = max(nx.connected_components(G), key=len)
    G_cc = G.subgraph(largest_cc)
    print("Graph is not connected")
    print("Largest connected component size:", len(G_cc))
    diameter = nx.approximation.diameter(G_cc)

print("Diameter:", diameter)

# Clustering
clustering = nx.average_clustering(G)
print("Average clustering:", clustering)

# Assortativity
assortativity = nx.degree_assortativity_coefficient(G)
print("Assortativity:", assortativity)

# Degree distribution
degrees = [d for _, d in G.degree()]

plt.hist(degrees, bins=50)
plt.xlabel("Degree")
plt.ylabel("Frequency")

plt.savefig(BASE_DIR.parent.parent / "results" / "assignment1" / "degree_distribution.png")
print("Degree plot saved")