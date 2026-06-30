from contagion import create_network, spread_step

G = create_network(num_verifiers=50, num_unintentional=20)

for i in range(20):
    changed = spread_step(G, threshold=0.05)
    print("Step", i, "changes:", changed)
    if changed==0:
        break
    
true = 0
false = 0
none = 0
for n in G.nodes():
    msg = G.nodes[n]["message"]
    if msg == "true":
        true += 1
    elif msg == "false":
        false += 1
    else:
        none += 1

print("\nFinal result")
print("True:", true)
print("False:", false)
print("No message:", none)