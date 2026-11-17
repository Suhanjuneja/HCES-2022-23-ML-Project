from pathlib import Path
import json
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'Suhan_Juneja_HCES_Research_Journal.pdf'
W, PAGE_H = A4

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='PaperTitle2', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=17, leading=20, alignment=TA_CENTER, textColor=colors.HexColor('#74243f'), spaceAfter=8))
styles.add(ParagraphStyle(name='Author2', parent=styles['Normal'], fontSize=9, leading=13, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle(name='Body2x', parent=styles['BodyText'], fontSize=9, leading=12, alignment=TA_JUSTIFY, spaceAfter=6))
styles.add(ParagraphStyle(name='H1x2', parent=styles['Heading2'], fontSize=12, leading=14, textColor=colors.HexColor('#74243f'), spaceBefore=7, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name='H2x2', parent=styles['Heading3'], fontSize=10, leading=12, textColor=colors.HexColor('#333333'), spaceBefore=5, spaceAfter=3, keepWithNext=True))
styles.add(ParagraphStyle(name='Caption2', parent=styles['Normal'], fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor('#444444'), spaceAfter=7))
styles.add(ParagraphStyle(name='Small2', parent=styles['Normal'], fontSize=8, leading=10, alignment=TA_LEFT, spaceAfter=4))

summary = json.loads((ROOT/'results/run_summary.json').read_text(encoding='utf-8'))
profiles = pd.read_csv(ROOT/'results/cluster_profiles.csv')
comp = pd.read_csv(ROOT/'results/model_comparison.csv')
km_stab = pd.read_csv(ROOT/'results/stability_summary.csv').iloc[0]
ward_stab = pd.read_csv(ROOT/'results/ward_stability_summary.csv').iloc[0]
pca = pd.read_csv(ROOT/'results/pca_explained_variance.csv')

story = []
def P(text, style='Body2x'):
    return Paragraph(text, styles[style])
def H(text):
    return P(text, 'H1x2')
def SH(text):
    return P(text, 'H2x2')
def fig(relpath, maxw=6.2*inch, maxh=2.7*inch):
    im = Image(str(ROOT/relpath))
    scale = min(maxw/im.imageWidth, maxh/im.imageHeight)
    im.drawWidth = im.imageWidth*scale
    im.drawHeight = im.imageHeight*scale
    return im
def make_table(data, widths=None, fs=8):
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#74243f')),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),fs),
        ('LEADING',(0,0),(-1,-1),fs+2),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#c9c9c9')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f1f3')]),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    return t

def decorate(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#74243f'))
    canvas.setFont('Helvetica-Bold', 8)
    if doc.page > 1:
        canvas.drawString(0.65*inch, PAGE_H-0.42*inch, 'ML APPLICATION ASSIGNMENT — JOURNAL-FORMAT SUBMISSION')
        canvas.setStrokeColor(colors.HexColor('#c9c9c9'))
        canvas.line(0.65*inch, PAGE_H-0.48*inch, W-0.65*inch, PAGE_H-0.48*inch)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(0.65*inch, 0.35*inch, 'Suhan Juneja | HCES 2022–23 | Problem 54')
    canvas.drawRightString(W-0.65*inch, 0.35*inch, f'Page {doc.page}')
    canvas.restoreState()

# PAGE 1 — title, abstract, introduction and related work
story += [Spacer(1, 0.18*inch),
    P('State and Rural–Urban Clustering of Household Consumption Expenditure in India using HCES 2022–23','PaperTitle2'),
    P('<b>Suhan Juneja</b><br/>Department of Computer Science, Ramanujan College, University of Delhi, New Delhi, India<br/>Roll No.: 24020570031 | Machine Learning (B.Sc. (H) Computer Science) | Problem No. 54<br/>Original Research Article','Author2'),
    Spacer(1, 6),
    P('<b>Abstract.</b> This study explores rural and urban monthly per-capita consumption expenditure (MPCE) across 36 Indian States and Union Territories using published estimates from the Household Consumption Expenditure Survey (HCES) 2022–23. Because unit-level microdata were not available for this submission, the original household budget-share segmentation question is explicitly reframed as aggregate State/UT profile clustering. Rural MPCE, urban MPCE and the percentage urban–rural gap are standardized. K-means and Ward agglomerative clustering are compared for k = 2–5 using silhouette scores. K-means initialization stability is assessed over 30 random seeds, and Ward sensitivity is assessed over 100 repeated 80% subsamples. Ward agglomerative clustering with k = 3 obtains the highest silhouette (0.445). The results describe regional aggregates only and cannot identify household types, dietary patterns or nutrition outcomes.'),
    P('<b>Keywords:</b> HCES 2022–23; MoSPI; MPCE; State/UT; PCA; K-means; hierarchical clustering; silhouette; India','Small2'),
    H('1. Introduction'),
    P('Household consumption expenditure is an important statistical indicator of material living conditions. India’s Ministry of Statistics and Programme Implementation (MoSPI), through the National Sample Survey Office (NSSO), publishes estimates from the Household Consumption Expenditure Survey. The 2022–23 report includes State/UT average monthly per-capita consumption expenditure for rural and urban sectors. This paper uses those published aggregates to examine whether States/UTs can be grouped by expenditure level and the relative rural–urban gap.'),
    P('The allocated project originally proposed household segmentation using budget shares for cereals, protein, processed food, fuel and services. Those variables require unit-level household records. Since the microdata could not be accessed, this project does not pretend to solve that household-level task. Instead, it presents a transparent, narrower analysis of State/UT aggregate expenditure profiles. The change in unit of analysis is a central limitation, not a minor technical detail.'),
    H('2. Related Work'),
    P('The official HCES report provides the statistical source for average MPCE and related State/UT comparisons. Principal component analysis (PCA) is a standard linear technique for representing correlated measurements in a lower-dimensional coordinate system. K-means partitions observations around centroids, while Ward hierarchical clustering successively merges groups to minimize within-cluster variance. The silhouette coefficient evaluates separation by comparing within-cluster and nearest-other-cluster distances. These metrics are exploratory and should be interpreted cautiously for a small set of aggregate observations.'),
    PageBreak()]

# PAGE 2 — data and EDA
story += [H('3. Dataset and Preprocessing'), SH('3.1 Source and observational unit'),
    P('The dataset contains 36 State/UT observations transcribed from Summary Statement 1, printed page S1, of MoSPI/NSSO NSS Report No. 591, <i>Survey on Household Consumption Expenditure: 2022–23</i>. The selected columns are the ordinary average MPCE values for rural and urban sectors. The separate “with imputation” columns are not used. The All-India row is excluded because it is a national aggregate, not a State/UT unit. The official report URL is listed in the references.'),
    SH('3.2 Variables and feature engineering'),
    P('The two source variables are Rural MPCE and Urban MPCE, in nominal rupees per person per month. Two derived quantities are calculated: absolute gap = Urban MPCE − Rural MPCE; percentage gap = 100 × (Urban MPCE − Rural MPCE) / Rural MPCE. The clustering feature vector contains rural MPCE, urban MPCE and percentage gap. The absolute gap is retained for descriptive interpretation but is not used as an additional model feature.'),
    SH('3.3 Data quality and preprocessing'),
    P('The analysis script checks that all required columns exist, that State/UT names are unique, that there are exactly 36 observations, and that the two MPCE variables are non-missing and positive. Derived gap columns are recalculated in code to avoid depending on stale values in the CSV. The three model features are z-score standardized using StandardScaler. No missing-value imputation is performed because the selected source table has complete entries.'),
    P('The source data are published estimates, not household microdata. No household sampling weights are applied in this aggregate-level exercise. Nominal MPCE is not adjusted for spatial price differences. These choices limit interpretation and are reported explicitly.'),
    H('4. Exploratory Data Analysis'),
    P('Exploratory summaries are saved in results/descriptive_statistics.csv. The analysis also ranks State/UTs by the derived percentage gap in results/state_profiles_ranked.csv. These outputs allow inspection of the feature ranges and unusual profiles before clustering. The rural–urban difference is not uniformly positive: the published table includes an exception where urban MPCE is below rural MPCE. This is retained rather than altered.'),
    P('The data are cross-sectional aggregates for a single survey round. They do not support causal claims or longitudinal trends. Because the number of observations is 36, even a visually clear cluster should be treated as a descriptive grouping rather than a stable population taxonomy.'),
    PageBreak()]

# PAGE 3 — methodology and setup
story += [H('5. Methodology'), SH('5.1 Standardization and PCA'),
    P('Let xᵢ ∈ R³ denote the standardized feature vector for State/UT i. Standardization is necessary because two features are rupee amounts and one is a percentage. PCA is fitted to the three standardized features and the first two principal components are used for visualization. PCA is not used to discard the third feature before clustering; both clustering algorithms operate on the complete three-dimensional standardized matrix.'),
    SH('5.2 Clustering algorithms'),
    P('K-means is fitted for k = 2, 3, 4 and 5, with a fixed seed and 50 initializations for the comparison run. Ward agglomerative clustering is fitted for the same k values. For each solution, the mean silhouette coefficient is computed on the standardized feature matrix. The highest score across the eight algorithm–k combinations is selected as the primary descriptive solution. Cluster identifiers are arbitrary and do not imply an ordinal ranking.'),
    SH('5.3 Validation and robustness'),
    P('The model comparison table provides a baseline comparison between centroid-based K-means and Ward hierarchical clustering across the same candidate k values. K-means initialization stability is assessed over 30 random seeds with 20 initializations per fit; pairwise adjusted Rand indices (ARI) are computed across 435 run pairs. Ward robustness is assessed separately through 100 repeated 80% subsamples without replacement. For each pair of Ward runs, ARI is computed only on State/UT observations present in both subsamples. This is a case-sensitivity diagnostic, not a survey-design bootstrap or external validation.'),
    P('A conventional supervised train/test split is not appropriate here: there is no prediction target, and the task is unsupervised grouping of a small, fixed set of published aggregates. Validation therefore combines silhouette comparison, an alternative-algorithm baseline, K-means initialization stability and Ward subsampling sensitivity. These internal checks do not replace external validation with independent survey rounds or unit-level data.'),
    H('6. Experimental Setup'),
    P('The project is implemented in Python using pandas, NumPy, scikit-learn, Matplotlib and ReportLab. The script resolves paths relative to its own location, validates the input table, regenerates all result CSV files and creates the figures. K-means comparison runs use a fixed seed of 42; Ward agglomerative clustering is deterministic for a fixed feature matrix and linkage. The run summary is stored as JSON. Exact environment package versions may vary; requirements.txt specifies minimum supported versions.'),
    P('Run from the repository root with: <font name="Courier">python -m pip install -r requirements.txt</font>, followed by <font name="Courier">python src/analysis.py</font>. Rebuild this PDF with <font name="Courier">python build_journal.py</font>.'),
    PageBreak()]

# PAGE 4 — results
km3 = float(comp[(comp.algorithm=='KMeans') & (comp.k==3)].silhouette.iloc[0])
story += [H('7. Results'), SH('7.1 Model comparison'),
    P(f'The highest silhouette score is obtained by Ward agglomerative clustering with k = {summary["selected_k"]} (score = {summary["selected_model_silhouette"]:.3f}). K-means at k = 3 obtains a silhouette score of {km3:.3f}. The alternative algorithm therefore provides a better internal separation score on this dataset. This model choice is based on the stated comparison criterion, not on a claim that the resulting groups are objectively “true”.'),
    make_table([['Algorithm','k','Silhouette']]+[[r.algorithm,str(r.k),f'{r.silhouette:.3f}'] for r in comp.itertuples(index=False)], widths=[2.5*inch,.6*inch,1.2*inch], fs=8),
    Spacer(1,7), fig('figures/model_comparison_silhouette.png', maxw=6.1*inch, maxh=2.5*inch),
    P('Fig. 1. Silhouette comparison for K-means and Ward agglomerative clustering.','Caption2'),
    SH('7.2 Final cluster profiles'),
    make_table([['Cluster','n','Rural MPCE','Urban MPCE','Gap %']]+[[str(int(r.Cluster)),str(int(r.Number_of_States_UTs)),f'{r.Rural_MPCE_Rs:,.0f}',f'{r.Urban_MPCE_Rs:,.0f}',f'{r.Urban_Rural_Gap_Percent:.1f}'] for r in profiles.itertuples(index=False)], widths=[.8*inch,.5*inch,1.25*inch,1.25*inch,1*inch], fs=8),
    P('Cluster 1 contains 26 State/UTs and has lower mean MPCE with a comparatively large percentage gap. Cluster 2 contains seven State/UTs, with higher rural MPCE and a smaller average gap. Cluster 3 contains three State/UTs and has the highest mean rural and urban MPCE. These are summaries of group averages; they should not be converted into value judgements about residents.'),
    fig('figures/rural_urban_mpce_clusters.png', maxw=6.1*inch, maxh=2.35*inch),
    P('Fig. 2. Rural versus urban MPCE by final Ward cluster.','Caption2'),
    PageBreak()]

# PAGE 5 — PCA and stability
story += [H('7. Results (continued)'), SH('7.3 PCA representation and stability'),
    P(f'The first two principal components explain {pca.iloc[0].explained_variance_ratio*100:.1f}% and {pca.iloc[1].explained_variance_ratio*100:.1f}% of standardized feature variance, respectively; together they explain {summary["pca_two_component_variance"]*100:.1f}%. The PCA plot is a two-dimensional visualization only. Clustering was fitted on all three standardized features.'),
    fig('figures/pca_cluster_projection.png', maxw=6.1*inch, maxh=2.45*inch),
    P('Fig. 3. PCA projection coloured by Ward cluster.','Caption2'),
    P(f'For the K-means baseline at k = {summary["selected_k"]}, 30 random-seed runs produce a mean pairwise ARI of {km_stab.mean_pairwise_ARI:.3f} (standard deviation {km_stab.std_pairwise_ARI:.3f}; range {km_stab.min_pairwise_ARI:.3f}–{km_stab.max_pairwise_ARI:.3f}).'),
    fig('figures/stability_ari_distribution.png', maxw=6.1*inch, maxh=2.15*inch),
    P('Fig. 4. Pairwise ARI distribution across 30 K-means baseline runs (435 run pairs).','Caption2'),
    P(f'Ward subsampling sensitivity across 100 runs (each using 80% of the 36 States/UTs) yields {int(ward_stab.pairwise_comparisons)} pairwise comparisons on overlapping observations. Mean pairwise ARI is {ward_stab.mean_pairwise_ARI_on_overlap:.3f} (SD {ward_stab.std_pairwise_ARI_on_overlap:.3f}; range {ward_stab.min_pairwise_ARI_on_overlap:.3f}–{ward_stab.max_pairwise_ARI_on_overlap:.3f}). This indicates that Ward assignments are sensitive to which aggregate units are included; the statistic is affected by the small sample and changing overlap.'),
    fig('figures/ward_subsample_stability_ari.png', maxw=6.1*inch, maxh=2.0*inch),
    P('Fig. 5. Ward clustering sensitivity: pairwise ARI on State/UTs shared by each pair of 80% subsamples.','Caption2'),
    PageBreak()]

# PAGE 6 — discussion, limitations, conclusion and references
story += [H('8. Discussion'),
    P('The comparison demonstrates why a single algorithm should not be assumed to be best in advance. Ward clustering has the highest silhouette among the tested candidates, while K-means provides a useful centroid-based baseline with generally stable solutions across random seeds. Ward subsampling sensitivity is less consistent, indicating that the selected grouping can change when a subset of the small set of aggregate observations is removed. The three clusters primarily distinguish combinations of expenditure level and relative rural–urban gap.'),
    P('The high PCA variance is not evidence of high predictive accuracy: PCA is descriptive dimensionality reduction, and the analysis has no target variable. Likewise, silhouette is an internal geometric criterion, not proof that the groupings correspond to social, economic or nutritional categories.'),
    H('9. Limitations and Ethical Interpretation'),
    P('(i) The unit of analysis is a State/UT aggregate, so within-State/UT household variation is hidden. (ii) The original household budget-share question is not answered because the available data do not include household-level category shares. (iii) No survey weights, design effects or standard errors are incorporated in this aggregate analysis. (iv) MPCE values are nominal and are not spatially price-adjusted. (v) Only one survey round is used. (vi) The number of observations is small (n = 36), and silhouette-based selection may change with feature engineering or alternative distance choices. (vii) Ward subsampling sensitivity is an internal case-sensitivity diagnostic, not a design-based bootstrap or population-level guarantee.'),
    H('10. Conclusion and Future Work'),
    P('This project builds a reproducible exploratory workflow for grouping 36 State/UTs using published rural and urban MPCE estimates from HCES 2022–23. Across K-means and Ward candidates with k = 2–5, Ward agglomerative clustering with k = 3 achieves the highest silhouette score (0.445). The resulting groups describe aggregate expenditure profiles and rural–urban differences. They are not household segments and do not directly describe nutrition, diet quality or food-budget allocations.'),
    P('Future work should use the official unit-level HCES files, document the survey design, apply appropriate weights, construct household-level expenditure shares and compare clustering under alternative feature sets. Further robustness work could use survey-design-aware uncertainty estimates and independent survey rounds where comparable data are available.'),
    H('Declarations'),
    P('<b>Data availability:</b> The 36-row analysis table and source notes are included in the repository. Source: MoSPI/NSSO NSS Report No. 591, Summary Statement 1. <b>Code availability:</b> Python analysis and PDF build scripts are included. <b>Conflict of interest:</b> The author declares no conflict of interest. <b>Funding:</b> No external funding is declared. <b>AI assistance:</b> AI tools assisted with drafting and code preparation. The student must independently review, run, verify and take responsibility for the final work.'),
    H('References'),
    P('[1] Ministry of Statistics and Programme Implementation (MoSPI), NSSO, <i>Survey on Household Consumption Expenditure: 2022–23</i>, NSS Report No. 591, Government of India, Summary Statement 1, p. S1. https://mospi.gov.in/sites/default/files/publication_reports/Report_591_HCES_2022-23New.pdf','Small2'),
    P('[2] J. MacQueen, “Some methods for classification and analysis of multivariate observations,” in <i>Proc. 5th Berkeley Symp. Math. Statist. Prob.</i>, 1967, pp. 281–297.','Small2'),
    P('[3] P. J. Rousseeuw, “Silhouettes: A graphical aid to the interpretation and validation of cluster analysis,” <i>Journal of Computational and Applied Mathematics</i>, vol. 20, pp. 53–65, 1987.','Small2'),
    P('[4] I. T. Jolliffe and J. Cadima, “Principal component analysis: A review and recent developments,” <i>Philosophical Transactions of the Royal Society A</i>, vol. 374, 2016.','Small2'),
    P('[5] F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” <i>Journal of Machine Learning Research</i>, vol. 12, pp. 2825–2830, 2011.','Small2'),
    H('Appendix: Reproducibility Checklist'),
    P('Repository contents include the published aggregate data CSV and source notes; analysis.py; build_journal.py; requirements.txt; README; generated result CSV/JSON files; and five figures. From the repository root: (1) install requirements; (2) run src/analysis.py; (3) run build_journal.py to regenerate this PDF. The supervisor field is omitted because no supervisor name was provided.'),
    P('<b>Important scope statement:</b> The results are ecological summaries at State/UT level. They must not be presented as household-level segmentation or nutrition findings.','Small2')]

# Single-column, full-width layout is intentional: it avoids clipped columns and overlapping figures.
doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=0.68*inch, leftMargin=0.68*inch,
                        topMargin=0.72*inch, bottomMargin=0.62*inch,
                        title='State and Rural–Urban Clustering of HCES 2022–23', author='Suhan Juneja')
doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
print(f'Created {OUT} ({OUT.stat().st_size} bytes)')
