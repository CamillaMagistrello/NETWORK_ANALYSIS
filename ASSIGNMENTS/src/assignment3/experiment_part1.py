from contagion import create_network, spread_step

for unintentional in [0, 10, 20, 50, 100, 200]:
    results = []
    for experiment in range(10):
        G = create_network(num_verifiers=50, num_unintentional=unintentional)
        for i in range(20):
            changed = spread_step(G, threshold=0.05)
            if changed == 0:
                break
        true = 0
        false = 0
        for n in G.nodes():
            msg = G.nodes[n]["message"]
            if msg == "true":
                true += 1
            elif msg == "false":
                false += 1
                
        total = G.number_of_nodes()
        results.append(false/total*100)

    average = sum(results)/len(results)
    print("Unintentional:", unintentional, "| Average fake news:", round(average,2), "%")