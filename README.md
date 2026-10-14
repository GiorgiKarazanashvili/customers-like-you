# Customers Like You — PCA or SVD

DS 5020 Mini-Project. GiftLane (fictional UK gift-ware retailer) wants:
1. A "Customers who bought this also bought..." box that runs as a fast nightly job.
2. One picture of the main customer groups for marketing.

**Team:** Giorgi Karazanashvili — solo (Data Engineer + ML Engineer).

## Success targets (J1)
Agreed before any modelling. The project succeeds if:

| # | Target | Measured by |
|---|--------|-------------|
| 1 | Compressed factors are **at least 20x smaller** than the dense customer x product matrix | MB of stored factors vs dense MB (DE5, ML5) |
| 2 | The nightly job (fit + score all products) runs in **under 60 seconds** on a laptop | Wall-clock time (ML4) |
| 3 | Recommendations **beat the best-seller baseline** on hit rate @10, on held-out purchases the model never saw | Hit rate @10, model vs top-10 best sellers (ML4) |
| 4 | The customer map shows **3 to 6 groups** that can be named from their top products and countries | Customer map figure (ML6) |

## Data
UCI Online Retail II — https://archive.ics.uci.edu/dataset/502/online+retail+ii (CC BY 4.0).
Not committed to Git. Download it and place it at `data/raw/online_retail_II.xlsx`.

Row count check (Step 0): **1,067,371 rows** (sheet "Year 2009-2010": 525,461; sheet "Year 2010-2011": 541,910).

## How to run
```
pip install -r requirements.txt
python src/build_matrix.py       # rebuilds the matrix from the raw file
jupyter notebook notebooks/analysis.ipynb
```
_(Updated as the project is built.)_

## Repository layout
```
data/raw/        raw Excel file (not committed)
data/processed/  train/test files, sparse matrix (not committed)
src/             pipeline scripts
notebooks/       analysis notebook
reports/         cleaning log, matrix report, memo, decision and contribution logs
figures/         plots and the customer map
```
