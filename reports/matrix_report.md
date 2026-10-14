# DE5 — Matrix Report

Customer x product matrix built from **training rows only**. Cell value = log(1 + total quantity the customer bought of that product).

| Measure | Value |
|---|---|
| Shape (customers x products) | 5,471 x 3,686 |
| Non-zero cells | 413,691 |
| Sparsity | 97.95% zeros |
| Average products per customer | 75.6 |
| Dense size (8-byte floats) | 161.3 MB |
| Sparse size (CSR: values + indices + pointers) | 5.0 MB |
| Dense / sparse | 32.4x |

## Product filter
Products in training data: 4,529. Kept (bought by at least 10 customers): 3,686.