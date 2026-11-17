"""
Suhan Juneja | HCES 2022-23 state/rural-urban clustering
Run from project root: python src/analysis.py
Input: data/hces_state_sector_mpce.csv
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hces_state_sector_mpce.csv"
OUT = ROOT / "results"
FIG = ROOT / "figures"
OUT.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
features = ["Rural_MPCE_Rs", "Urban_MPCE_Rs", "Urban_Rural_Gap_Percent"]
X = StandardScaler().fit_transform(df[features])

scores = {}
for k in range(2, 6):
    labels = KMeans(n_clusters=k, random_state=42, n_init=20).fit_predict(X)
    scores[k] = silhouette_score(X, labels)
best_k = max(scores, key=scores.get)
km = KMeans(n_clusters=best_k, random_state=42, n_init=20)
df["Cluster"] = km.fit_predict(X) + 1

pca = PCA(n_components=2, random_state=42)
pcs = pca.fit_transform(X)
df["PC1"], df["PC2"] = pcs[:, 0], pcs[:, 1]
df.to_csv(OUT / "state_cluster_assignments.csv", index=False)
pd.DataFrame([{"k": k, "silhouette_score": v} for k, v in scores.items()]).to_csv(OUT / "silhouette_scores.csv", index=False)
df.groupby("Cluster")[features].mean().round(2).to_csv(OUT / "cluster_profiles.csv")
pd.DataFrame({"component": ["PC1", "PC2"], "explained_variance_ratio": pca.explained_variance_ratio_}).to_csv(OUT / "pca_explained_variance.csv", index=False)

plt.figure(figsize=(10, 6))
for cluster, g in df.groupby("Cluster"):
    plt.scatter(g["Rural_MPCE_Rs"], g["Urban_MPCE_Rs"], label=f"Cluster {cluster}")
    for _, r in g.iterrows():
        plt.annotate(r["State_UT"], (r["Rural_MPCE_Rs"], r["Urban_MPCE_Rs"]), fontsize=6)
plt.xlabel("Rural MPCE (Rs/person/month)"); plt.ylabel("Urban MPCE (Rs/person/month)")
plt.title("State/UT rural-urban MPCE clusters"); plt.legend(); plt.tight_layout()
plt.savefig(FIG / "rural_urban_mpce_clusters.png", dpi=180); plt.close()

plt.figure(figsize=(8, 5))
plt.bar([str(k) for k in scores], list(scores.values()))
plt.xlabel("k"); plt.ylabel("Silhouette score"); plt.title("K-means model selection")
plt.tight_layout(); plt.savefig(FIG / "silhouette_scores.png", dpi=180); plt.close()

plt.figure(figsize=(8, 5))
for cluster, g in df.groupby("Cluster"):
    plt.scatter(g["PC1"], g["PC2"], label=f"Cluster {cluster}")
    for _, r in g.iterrows():
        plt.annotate(r["State_UT"], (r["PC1"], r["PC2"]), fontsize=6)
plt.xlabel("PC1"); plt.ylabel("PC2"); plt.title("PCA projection"); plt.legend(); plt.tight_layout()
plt.savefig(FIG / "pca_cluster_projection.png", dpi=180); plt.close()

print(f"Selected k={best_k}; silhouette={scores[best_k]:.3f}")
print("Results saved under results/ and figures/")
