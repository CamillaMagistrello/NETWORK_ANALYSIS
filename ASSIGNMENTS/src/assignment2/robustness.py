import networkx as nx
import matplotlib.pyplot as plt
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def giant_component(G):
    if len(G) == 0:
        return 0, G
    largest = max(nx.connected_components(G), key=len)
    return len(largest), G.subgraph(largest).copy()

def attack(G, strategy, step=0.05):
    G = G.copy()
    N = G.number_of_nodes()
    results = []

    while G.number_of_nodes() > 0:
        remove_number = min(max(1, int(G.number_of_nodes() * step)), G.number_of_nodes())

        if strategy == "random":
            nodes = random.sample(list(G.nodes()), remove_number)

        elif strategy == "degree":
            nodes = [n for n, d in sorted(G.degree(), key=lambda x: x[1], reverse=True)[:remove_number]]

        elif strategy == "pagerank":
            pr = nx.pagerank(G)
            nodes = sorted(pr, key=pr.get, reverse=True)[:remove_number]

        elif strategy == "betweenness":
            k = min(500, G.number_of_nodes())
            bc = nx.betweenness_centrality(G, k=k)
            nodes = sorted(bc, key=bc.get, reverse=True)[:remove_number]

        G.remove_nodes_from(nodes)
        size, G = giant_component(G)
        results.append(size / N)

    return results

def run(graph_file, output_file):

    G = nx.read_gexf(BASE_DIR.parent.parent / "data" / graph_file)

    print("Running attacks...")

    random_result = attack(G, "random")
    degree_result = attack(G, "degree")
    pagerank_result = attack(G, "pagerank")
    betweenness_result = attack(G, "betweenness")

    plt.figure(figsize=(10,6))

    plt.plot(random_result, label="Random")
    plt.plot(degree_result, label="Degree")
    plt.plot(pagerank_result, label="PageRank")
    plt.plot(betweenness_result, label="Betweenness")

    plt.xlabel("Percentage of removed nodes")
    plt.ylabel("G/N")
    plt.legend()

    plt.savefig(BASE_DIR.parent.parent / "results" / "assignment2" / output_file)

    plt.close()

    print("Saved")