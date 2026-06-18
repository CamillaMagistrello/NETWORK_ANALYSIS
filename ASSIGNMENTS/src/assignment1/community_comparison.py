import csv
from sklearn.metrics import normalized_mutual_info_score
from sklearn.metrics import adjusted_rand_score
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS = BASE_DIR.parent.parent / "results" / "assignment1"

def load_partition(file):
    partition = {}
    with open(file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            partition[row["node"]] = int(row["community"])
    return partition

leiden = load_partition(RESULTS / "leiden.csv")

louvain = load_partition(
    RESULTS / "louvain.csv"
)


nodes = list(leiden.keys())


leiden_labels = [
    leiden[n]
    for n in nodes
]


louvain_labels = [
    louvain[n]
    for n in nodes
]

nmi = normalized_mutual_info_score(leiden_labels, louvain_labels)
ari = adjusted_rand_score(leiden_labels, louvain_labels)

print("====================")
print("COMMUNITY COMPARISON")
print("====================")

print("NMI:", nmi)
print("ARI:", ari)