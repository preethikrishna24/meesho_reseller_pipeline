# Part 1 SQL Outputs

These CSVs are generated from `data/meesho_reseller.db` by `part1_sql/run_queries.py`.

- `monthly_category_revenue.csv` — 15 rows; direct input to Parts 2 and 4.
- `region_revenue.csv` — revenue and order count by region.
- `top_resellers.csv` — top five resellers with total spend greater than INR 50000.
- `zero_order_resellers.csv` — resellers with no matching order rows.
- `zero_order_count_demo.csv` — demonstrates `COUNT(*) = 1` versus `COUNT(order_id) = 0` for RS024. `COUNT(*)` is wrong for detecting a zero-match LEFT JOIN because the unmatched reseller still produces one NULL-extended row.
- `june_delivered_aov.csv` — June Delivered-only AOV.

To regenerate all outputs:

```bash
python data/generate_dataset.py
python part1_sql/run_queries.py
```
