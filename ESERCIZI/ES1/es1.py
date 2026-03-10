# pip install networkx matplotlib

import sys
import networkx as nx
import matplotlib.pyplot as plt


# Example 1: Zachary's Karate Club graph
def karate_graph_example():
    print("Zachary’s Karate Club graph")

    G = nx.karate_club_graph()

    print("Node Degree")
    for v in G:
        print(f"{v:4} {G.degree(v):6}")

    # Draw the graph
    nx.draw_circular(G, with_labels=True)
    plt.show()


# Example 2: Expected Degree Graph
def expected_degree_example():
    print("Expected Degree Sequence")

    # make a random graph of 500 nodes with expected degree 50
    n = 500
    p = 0.1
    w = [p * n for i in range(n)]

    G = nx.expected_degree_graph(w)

    print("Degree histogram")
    print("degree (#nodes) ****")

    dh = nx.degree_histogram(G)

    for i, d in enumerate(dh):
        print(f"{i:2} ({d:2}) {'*' * d}")

    # draw the graph
    plt.figure()
    nx.draw(G, node_size=20)
    plt.title("Expected Degree Graph")
    plt.show()

    # plot the degree distribution
    degrees = [d for n, d in G.degree()]

    plt.figure()
    plt.hist(degrees)
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of nodes")
    plt.show()


# ---- run example 1 and save output ----
with open("ES1/karate_output.txt", "w") as f:
    old_stdout = sys.stdout
    sys.stdout = f
    karate_graph_example()
    sys.stdout = old_stdout


# ---- run example 2 and save output ----
with open("ES1/expected_degree_output.txt", "w") as f:
    old_stdout = sys.stdout
    sys.stdout = f
    expected_degree_example()
    sys.stdout = old_stdout