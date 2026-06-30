import networkx as nx
from pathlib import Path
from robustness import run

BASE_DIR = Path(__file__).resolve().parent
G = nx.read_gexf(BASE_DIR.parent.parent / "data" / "anime_network.gexf")

print("Original")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

top_nodes = sorted(G.degree(), key=lambda x:x[1], reverse=True)[:3]
for node,degree in top_nodes:
    neighbors = list(G.neighbors(node))
    for i in range(len(neighbors)):
        for j in range(i+1,len(neighbors)):
            if not G.has_edge(neighbors[i],neighbors[j]):
                G.add_edge(neighbors[i], neighbors[j])
                
print("\nAfter adding edges")
print("Nodes:",G.number_of_nodes())
print("Edges:",G.number_of_edges())

nx.write_gexf(G, BASE_DIR.parent.parent / "data" / "anime_network_improved.gexf")
print("Improved graph saved")

def critical_threshold(G):
    degrees = [d for _, d in G.degree()]
    k1 = sum(degrees) / len(degrees)
    k2 = sum(d*d for d in degrees) / len(degrees)
    fc = 1 - 1 / ((k2 / k1) - 1)
    return k1, k2, fc

k1, k2, fc = critical_threshold(G)
print("First moment:", k1)
print("Second moment:", k2)
print("fc:", fc)

run("anime_network_improved.gexf", "robustness_improved.png")