import networkx as nx
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def create_network(num_verifiers=50, num_unintentional=10):
    G = nx.read_gexf(BASE_DIR.parent.parent / "data" / "anime_network.gexf")
    nodes = list(G.nodes())
    for n in nodes:
        G.nodes[n]["type"] = "normal"
        G.nodes[n]["message"] = None

    verifiers = random.sample(nodes, num_verifiers)
    for v in verifiers:
        G.nodes[v]["type"] = "verifier"
        G.nodes[v]["message"] = "true"

    unintentional = sorted(G.degree(), key=lambda x:x[1], reverse=True)[:num_unintentional]
    unintentional = [n for n,d in unintentional]
    for u in unintentional:
        G.nodes[u]["type"] = "unintentional"
    return G

def spread_step(G, threshold=0.3):
    changes = {}
    for node in G.nodes():
        if G.nodes[node]["message"] is not None:
            continue

        neighbors = list(G.neighbors(node))
        if len(neighbors)==0:
            continue

        true_count = 0
        false_count = 0
        for n in neighbors:
            if G.nodes[n]["message"]=="true":
                true_count += 1
            elif G.nodes[n]["message"]=="false":
                false_count += 1

        if max(true_count, false_count) / len(neighbors) >= threshold:
            if G.nodes[node]["type"]=="unintentional":
                if true_count >= false_count:
                    changes[node]="false"
            else:
                if true_count >= false_count:
                    changes[node]="true"
                else:
                    changes[node]="false"

    for node,msg in changes.items():
        G.nodes[node]["message"]=msg

    return len(changes)