# Customers Like You — PCA or SVD

DS 5020 Mini-Project. GiftLane (a fictional UK gift-ware retailer) asked for:
1. A "Customers who bought this also bought..." box that runs as a fast nightly job.
2. One picture of the main customer groups for marketing.

**Team:** Giorgi Karazanashvili, working solo (Data Engineer and ML Engineer).

## Success targets (J1)
Set before any modelling. The project succeeds if:

| # | Target | Result |
|---|--------|--------|
| 1 | Stored factors are at least 20x smaller than the dense customer x product matrix | 7.3 MB vs 161.3 MB (22x) |
| 2 | The nightly job runs in under 60 seconds on a laptop | About 1 second |
| 3 | Recommendations beat the best-seller baseline on hit rate @10, on purchases the model never saw | 38.3% vs 27.0% |
| 4 | The customer map shows 3 to 6 groups that can be named from their products and countries | 4 named groups |

## Data
UCI Online Retail II: https://archive.ics.uci.edu/dataset/502/online+retail+ii (CC BY 4.0).
Not committed to Git. Download it and place it at `data/raw/online_retail_II.xlsx`.

Row count check (Step 0): **1,067,371 rows** (sheet "Year 2009-2010": 525,461; sheet "Year 2010-2011": 541,910).

## How to run
```
pip install -r requirements.txt
python src/build_matrix.py                # cleans the data and rebuilds the matrix (about 1 minute)
jupyter notebook notebooks/analysis.ipynb # then Run All
```
`build_matrix.py` prints the data profile, the rows removed by each cleaning rule and the matrix report.
The notebook uses a fixed random seed (42), so results are the same on every run.

## Repository layout
```
src/build_matrix.py        data cleaning, time split and sparse matrix (DE1-DE6)
notebooks/analysis.ipynb   method choice, k selection, recommender, evaluation, PCA vs SVD, customer map (ML1-ML6)
reports/                   data profile, cleaning log, matrix report, memo, individual reflection
figures/                   k selection curve and customer map
decision_log.md            every decision and its reason
contribution_log.md        who did what, with evidence
data/                      raw and processed data (not committed)
```
