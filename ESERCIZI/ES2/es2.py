import sys
import networkx as nx

# redirect all prints to a file
sys.stdout = open("ES2/output.txt", "w")

def centrality_example():

    G = nx.karate_club_graph()

    bet = nx.betweenness_centrality(G)
    clo = nx.closeness_centrality(G)

    top_bet = sorted(bet.items(), key=lambda x: x[1], reverse=True)[:10]
    top_clo = sorted(clo.items(), key=lambda x: x[1], reverse=True)[:10]

    print("Top 10 nodes by Betweenness Centrality")
    for node, value in top_bet:
        print(f"Node {node}: {value:.4f}")

    print("\nTop 10 nodes by Closeness Centrality")
    for node, value in top_clo:
        print(f"Node {node}: {value:.4f}")


centrality_example()