# DE2 — Cleaning Log

Rules applied in this order:

| Rule | Rows removed | Rows left | Reason |
|---|---|---|---|
| Start | 0 | 1,067,371 | Both sheets combined |
| Sheet overlap | 22,523 | 1,044,848 | Sheet 1 repeats 1–9 Dec 2010 lines that are also in sheet 2; keep one copy |
| Missing customer ID | 235,287 | 809,561 | Cannot place a purchase in a customer row |
| Cancellations | 18,446 | 791,115 | Invoice starting with 'C' is a cancelled order, not a purchase |
| Quantity <= 0 | 0 | 791,115 | Returns and stock adjustments |
| Price <= 0 | 70 | 791,045 | Free items, write-offs and bad-debt entries |
| Non-product codes | 2,858 | 788,187 | POST, DOT, M, D, BANK CHARGES, gift vouchers etc. are fees, not products |
| Exact duplicates | 11,610 | 776,577 | Identical lines (same invoice, product, quantity, time) entered twice |

Customers left: 5,852  
Products left: 4,619  
Date range: 2009-12-01 to 2011-12-09