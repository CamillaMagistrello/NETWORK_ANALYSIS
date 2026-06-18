import pandas as pd
from pathlib import Path
from sklearn.metrics import normalized_mutual_info_score
from sklearn.metrics import adjusted_rand_score

BASE_DIR = Path(__file__).resolve().parent
RESULTS = BASE_DIR.parent.parent / "results" / "assignment1"

louvain = pd.read_csv(RESULTS / "louvain.csv")
leiden = pd.read_csv(RESULTS / "leiden.csv")
louvain = louvain.sort_values("anime")
leiden = leiden.sort_values("anime")
nmi = normalized_mutual_info_score(louvain["community"], leiden["community"])
ari = adjusted_rand_score(louvain["community"], leiden["community"])

print("====================")
print("COMMUNITY EVALUATION")
print("====================")
print("NMI:")
print(nmi)

print("\nARI:")
print(ari)

with open(RESULTS / "evaluation.txt", "w", encoding="utf-8") as file:
    file.write("====================\n")
    file.write("COMMUNITY EVALUATION\n")
    file.write("====================\n\n")

    file.write(f"NMI: {nmi}\n")
    file.write(f"ARI: {ari}\n")

print("\nResults saved in:")
print(RESULTS)