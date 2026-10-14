from pathlib import Path
import numpy as np
import pandas as pd
import scipy.sparse as sp

RAW = Path("data/raw/online_retail_II.xlsx")
OUT = Path("data/processed")

PRODUCT_CODE = r"^\d{5}[A-Za-z]*$"   # 5 digits + optional variant letters
TEST_MONTHS = 2
MIN_CUSTOMERS_PER_PRODUCT = 10


def load():
    sheets = pd.read_excel(RAW, sheet_name=None, dtype={"Invoice": str, "StockCode": str})
    frames = []
    for i, df in enumerate(sheets.values()):
        df["sheet"] = i
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)

    # DE1: row counts, column types, missing values
    print(f"Loaded {len(df):,} rows; per sheet: {df['sheet'].value_counts().sort_index().tolist()}")
    print(pd.DataFrame({"type": df.dtypes.astype(str), "missing": df.isna().sum()}).drop("sheet"))
    return df


def clean(df):
    rules = [
        ("Sheet overlap (1-9 Dec 2010 in both sheets)",
         lambda d: ~((d["sheet"] == 0) & (d["InvoiceDate"] >= "2010-12-01"))),
        ("Missing customer ID", lambda d: d["Customer ID"].notna()),
        ("Cancellations", lambda d: ~d["Invoice"].str.startswith("C")),
        ("Quantity <= 0", lambda d: d["Quantity"] > 0),
        ("Price <= 0", lambda d: d["Price"] > 0),
        ("Non-product codes", lambda d: d["StockCode"].str.match(PRODUCT_CODE)),
        ("Exact duplicates", lambda d: ~d.drop(columns="sheet").duplicated()),
    ]
    for name, keep in rules:
        before = len(df)
        df = df[keep(df)]
        print(f"  {name}: removed {before - len(df):,}, left {len(df):,}")

    df = df.drop(columns="sheet").copy()
    df["Customer ID"] = df["Customer ID"].astype(int)
    return df


def split(df):
    cutoff = (df["InvoiceDate"].max() - pd.DateOffset(months=TEST_MONTHS)).normalize()
    print(f"Test period starts {cutoff:%Y-%m-%d}")
    return df[df["InvoiceDate"] < cutoff], df[df["InvoiceDate"] >= cutoff]


def build_matrix(train):
    buyers = train.groupby("StockCode")["Customer ID"].nunique()
    train = train[train["StockCode"].isin(buyers[buyers >= MIN_CUSTOMERS_PER_PRODUCT].index)]

    customers = np.sort(train["Customer ID"].unique())
    products = np.sort(train["StockCode"].unique())
    cust_idx = pd.Series(range(len(customers)), index=customers)
    prod_idx = pd.Series(range(len(products)), index=products)

    qty = train.groupby(["Customer ID", "StockCode"])["Quantity"].sum().reset_index()
    A = sp.csr_matrix(
        (np.log1p(qty["Quantity"].to_numpy(dtype=float)),
         (qty["Customer ID"].map(cust_idx), qty["StockCode"].map(prod_idx))),
        shape=(len(customers), len(products)),
    )

    names = train.drop_duplicates("StockCode").set_index("StockCode")["Description"]
    cust_map = pd.DataFrame({"idx": range(len(customers)), "Customer ID": customers})
    prod_map = pd.DataFrame({"idx": range(len(products)), "StockCode": products,
                             "Description": names.reindex(products).to_numpy()})
    return A, cust_map, prod_map, cust_idx, prod_idx


def hold_out(train, test, cust_idx, prod_idx):
    # Test purchases of products the customer never bought before the cut-off
    seen = train[["Customer ID", "StockCode"]].drop_duplicates()
    pairs = test[["Customer ID", "StockCode"]].drop_duplicates()
    pairs = pairs[pairs["Customer ID"].isin(cust_idx.index) & pairs["StockCode"].isin(prod_idx.index)]
    new = pairs.merge(seen, how="left", indicator=True)
    new = new[new["_merge"] == "left_only"]
    return pd.DataFrame({"cust_idx": new["Customer ID"].map(cust_idx).to_numpy(),
                         "prod_idx": new["StockCode"].map(prod_idx).to_numpy()})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = clean(load())
    train, test = split(df)
    A, cust_map, prod_map, cust_idx, prod_idx = build_matrix(train)
    targets = hold_out(train, test, cust_idx, prod_idx)

    train.to_pickle(OUT / "train.pkl")
    test.to_pickle(OUT / "test.pkl")
    sp.save_npz(OUT / "A_log.npz", A)
    cust_map.to_csv(OUT / "customers.csv", index=False)
    prod_map.to_csv(OUT / "products.csv", index=False)
    targets.to_csv(OUT / "test_targets.csv", index=False)

    # DE5: matrix report
    m, n = A.shape
    sparse_mb = (A.data.nbytes + A.indices.nbytes + A.indptr.nbytes) / 1e6
    print(f"Matrix: {m:,} x {n:,}, {A.nnz:,} non-zeros, sparsity {1 - A.nnz / (m * n):.2%}")
    print(f"Memory: dense {m * n * 8 / 1e6:.1f} MB, sparse {sparse_mb:.1f} MB")
    print(f"Evaluation customers: {targets['cust_idx'].nunique():,}, held-out pairs: {len(targets):,}")


if __name__ == "__main__":
    main()
