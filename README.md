# State and Rural–Urban Clustering of HCES 2022–23

**Student:** Suhan Juneja  
**Roll No.:** 24020570031  
**Institution:** Ramanujan College, University of Delhi  
**Course:** Machine Learning, B.Sc. (H) Computer Science  
**Allocated problem:** 54 — Household consumption-pattern segmentation from HCES 2022–23

## Project scope — read before interpreting results

The original allocation describes household-level segmentation using food and non-food budget shares. Unit-level HCES microdata were not available for this project. The submitted analysis therefore uses the **published State/UT aggregate MPCE table** from HCES 2022–23 and clusters 36 State/UT rural–urban expenditure profiles. It does **not** perform household-level segmentation and it does not measure nutrition, diet quality, or category-level budget shares. Do not describe the clusters as household types.

## Research question

Can Indian States and Union Territories be grouped using rural MPCE, urban MPCE, and the percentage difference between them?

## Data source

MoSPI/NSSO, *Survey on Household Consumption Expenditure: 2022–23*, NSS Report No. 591, Summary Statement 1, printed page S1. The CSV transcribes the ordinary Average MPCE rural and urban columns, not the separate “with imputation” columns. The All-India aggregate is excluded. Source URL:

https://mospi.gov.in/sites/default/files/publication_reports/Report_591_HCES_2022-23New.pdf

See `data/source_and_variable_notes.txt` for the data dictionary and scope limitations.

## Methods

- Data checks: 36 rows, unique State/UT names, positive non-missing MPCE values.
- Feature engineering: absolute urban–rural gap and percentage gap.
- Preprocessing: z-score standardization of rural MPCE, urban MPCE, and percentage gap.
- Dimensionality reduction: PCA for a two-dimensional visualization; clustering uses all three standardized features.
- Model comparison: K-means and Ward agglomerative clustering for k = 2, 3, 4, 5.
- Internal validation: silhouette coefficient.
- K-means initialization stability: 30 random-seed runs and 435 pairwise adjusted Rand index (ARI) comparisons.
- Ward subsampling sensitivity: 100 repeated 80% subsamples without replacement; pairwise ARI is calculated only for State/UTs shared by each pair of runs (4,950 comparisons). This is a case-sensitivity diagnostic, not a survey-design bootstrap or external validation.

The current run selects **Ward agglomerative clustering, k = 3**, with silhouette **0.445**. K-means at k = 3 is retained as a baseline (silhouette approximately 0.406). The K-means initialization stability mean pairwise ARI is approximately 0.975 (SD approximately 0.094). Ward subsampling sensitivity mean pairwise ARI is approximately 0.535 (SD approximately 0.309). The Ward result indicates noticeable sensitivity to which aggregate observations are included. These are exploratory internal diagnostics on only 36 aggregate observations, not external validation.

## Repository structure

```text
Suhan_Juneja_HCES_Project/
├── README.md
├── requirements.txt
├── .gitignore
├── CITATION.cff
├── Suhan_Juneja_HCES_Research_Journal.pdf
├── build_journal.py
├── data/
│   ├── hces_state_sector_mpce.csv
│   └── source_and_variable_notes.txt
├── src/
│   └── analysis.py
├── results/
│   ├── descriptive_statistics.csv
│   ├── state_profiles_ranked.csv
│   ├── model_comparison.csv
│   ├── silhouette_scores.csv
│   ├── stability_summary.csv
│   ├── ward_stability_summary.csv
│   ├── state_cluster_assignments.csv
│   ├── cluster_profiles.csv
│   ├── pca_explained_variance.csv
│   └── run_summary.json
└── figures/
    ├── rural_urban_mpce_clusters.png
    ├── model_comparison_silhouette.png
    ├── pca_cluster_projection.png
    └── stability_ari_distribution.png
```

## Run on Windows / VS Code

Open this folder in VS Code. In Terminal → New Terminal, run:

```powershell
python -m pip install -r requirements.txt
python src/analysis.py
```

To rebuild the journal PDF after rerunning the analysis:

```powershell
python build_journal.py
```

The script writes regenerated tables to `results/` and plots to `figures/`. Run commands from the repository root (the folder containing `requirements.txt`).

## Reproducibility notes

- K-means comparison uses `random_state=42` and `n_init=50`.
- K-means initialization stability is evaluated across 30 random seeds with `n_init=20`.
- Ward subsampling sensitivity is evaluated across 100 repeated 80% subsamples without replacement; ARI is calculated on overlapping State/UTs. This is not a survey-design bootstrap or external validation.
- Ward linkage is deterministic for a fixed feature matrix and cluster count.
- No supervised train/test split is used because there is no target variable; the task is unsupervised clustering. Internal silhouette comparison, K-means initialization stability and Ward subsampling sensitivity are used instead.
- Cluster numbers are arbitrary labels; they do not rank States/UTs.

## Limitations

The dataset is aggregate and small (n = 36). No household-level records, survey weights, standard errors, food-group budget shares, nutritional indicators, or price-parity adjustments are used. The analysis is cross-sectional and descriptive. Results must not be generalized to individual households or treated as causal evidence.

## GitHub upload

This folder is prepared as a repository. To publish it, create a new repository on GitHub, then either upload the contents of this folder through **Add file → Upload files**, or use Git from this folder:

```bash
git init
git add .
git commit -m "Add HCES 2022-23 clustering project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with the URL of the repository you create. Do not upload any restricted microdata; this project contains only published aggregate values.
