# Narrative Report

## Worked narrative 1 — May Ethnic Wear

**Context:** Fact — Ethnic Wear revenue is measured from April to May 2026, comparing INR 104520.77 in April with INR 185107.61 in May.

**Insight:** Fact — Ethnic Wear revenue increased **77.1% Month-on-Month**, so the category crosses the 8.0% significance threshold and is flagged.

**Implication:** Hypothesis — the increase may reflect stronger demand, assortment changes, pricing, or other commercial drivers; the manager should next review May Ethnic Wear sales mix and operational availability against April before deciding whether the increase is sustainable.

### Refinement self-score
- **Specificity:** Pass — the narrative names Ethnic Wear, April, May, and the exact 77.1% change and verified revenues.
- **Audience fit:** Pass — it is written as a concise manager-facing update rather than a technical explanation.
- **Completeness:** Pass — Context, Insight, and Implication are all present and explicitly labeled.
- **Actionability:** Pass — it directs the manager to review May sales mix and operational availability against April.

## Worked narrative 2 — June Ethnic Wear

**Context:** Fact — Ethnic Wear revenue is measured from May to June 2026, comparing INR 185107.61 in May with INR 76371.53 in June.

**Insight:** Fact — Ethnic Wear revenue decreased **-58.74% Month-on-Month**, so the category crosses the 8.0% significance threshold in the negative direction and is flagged.

**Implication:** Hypothesis — the decline may reflect weaker demand, assortment or pricing changes, or operational availability; the manager should next review June Ethnic Wear sales mix and operational availability against May to identify the immediate driver and determine a corrective action.

### Refinement self-score
- **Specificity:** Pass — the narrative names Ethnic Wear, May, June, and the exact -58.74% change and verified revenues.
- **Audience fit:** Pass — it focuses on what a regional/category manager should know and do next.
- **Completeness:** Pass — Context, Insight, and Implication are all present and explicitly labeled.
- **Actionability:** Pass — it directs the manager to compare June with May on sales mix and operational availability.

## Chart-choice justification

### 1. Which month had the highest total revenue?
Use a **column chart** because this is a univariate comparison of one measure (total revenue) across a categorical month dimension. April is INR 419417.43, May is INR 444594.25, and June is INR 398055.24. A zero-based y-axis makes the magnitude comparison honest, and three columns make the message readable within 10 seconds; no legend is needed because there is only one series and 3D should be avoided.

### 2. What percentage share does Ethnic Wear represent of April's total revenue?
Use a **doughnut chart** for this part-to-whole question because it communicates one bivariate composition relationship: Ethnic Wear's INR 104520.77 is 24.92% of April's INR 419417.43. The single highlighted share can be read quickly, although a simple labeled bar would also be defensible when precise comparison is more important; avoid unnecessary 3D effects and keep the labels explicit.

### 3. How do the four regions compare on total revenue?
Use a **horizontal bar chart** because this is a univariate comparison of total revenue across four region categories. The values are North INR 337125.46, West INR 333106.33, South INR 316736.68, and East INR 275098.45. A zero-based x-axis supports honest magnitude comparison, the four bars communicate the message within 10 seconds, and no legend is needed because there is one series.

## Masked top-reseller narrative

Fact — the Part 1 top-reseller query identifies five resellers above INR 50000 in total spend. In descending spend order, the West region contains **ALIAS-19** at INR 75295.09 and **ALIAS-22** at INR 73882.33; the South region contains **ALIAS-12** at INR 69936.46; the North region contains **ALIAS-06** at INR 64238.97 and **ALIAS-05** at INR 61825.02. These are verified Part 1 values.

Implication (Hypothesis) — managers should review the regional mix and operating patterns associated with these coded resellers before drawing conclusions about causes or expanding the approach to other reseller cohorts.

The final text uses only coded aliases for reseller identity. `assert_no_raw_names_leak` must return `True` for this narrative and `False` for a negative test that contains `Mumbai Reseller 1` verbatim.
