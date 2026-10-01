# Meesho Reseller Growth & Alert Intelligence Pipeline

A small, deterministic, offline reseller-growth monitoring pipeline covering SQL analytics, Python guardrails, stakeholder narrative generation, and a human-reviewed mock agent runner.

## What this repository demonstrates

- **Part 1 — SQL Business Query Engine:** computes verified monthly/category revenue, regional performance, top-reseller spend, zero-order resellers, and June Delivered AOV.
- **Part 2 — Python Guardrail & Growth Detection:** turns “significant change” into an explicit 8% rule, handles the exact boundary as human escalation, and validates incoming revenue feeds.
- **Part 3 — Reliable Narrative Layer:** uses a deterministic template-fill path, explicit Context → Insight → Implication structure, validation checks, and reseller-name masking.
- **Part 4 — Agentic Workflow:** connects the Parts in a guarded Intake → Summary → Report Draft → Validate flow, caps drafts at three flagged categories, suppresses additional alerts for manual review, and holds all drafts for human approval.

The entire project runs locally with **zero API keys, paid services, hosted services, or LLM calls**.

## Repository structure

```text
data/
  generate_dataset.py
  resellers.csv
  orders.csv
  meesho_reseller.db
part1_sql/
  queries.sql
  run_queries.py
  output/*.csv
  output/README.md
part2_engine/
  growth_engine.py
  test_growth_engine.py
  fixtures/corrupted_feed.csv
  fixtures/monthly_category_revenue.csv
part3_narrative/
  prompt_pack.md
  narrative_report.md
  masking.py
  narrative.py
  test_masking.py
part4_agent/
  agent_spec.md
  mock_agent_runner.py
  test_mock_agent_runner.py
README.md
.gitignore
```

## Prerequisites

Python 3.9+ is sufficient; the implementation uses only the Python standard library. SQLite is accessed through Python's built-in `sqlite3` module. No third-party packages are required.

## Run the pipeline in order

Run all commands from the repository root.

### Step 1 — Regenerate the seeded dataset

The supplied generator uses `random.Random(42)`, the required reseller/category/month definitions, weights, and 300 orders per month.

```bash
python data/generate_dataset.py
```

This regenerates:

- `data/resellers.csv` — 24 resellers
- `data/orders.csv` — 900 orders, 300 each for April, May, and June 2026
- `data/meesho_reseller.db` — SQLite database containing the same data

The generator reports `RS024` as the zero-order reseller.

### Step 2 — Run Part 1 SQL

```bash
python part1_sql/run_queries.py
```

This writes the required SQL outputs under `part1_sql/output/`.

The most important handoff file is:

```text
part1_sql/output/monthly_category_revenue.csv
```

It contains exactly the four required columns:

```text
month,category,revenue,n_orders
```

### Step 3 — Run Part 2 tests

```bash
cd part2_engine
python -m unittest -v
cd ..
```

The tests cover the required April→May, May→June, exact 8% boundary, corrupted-feed validation, and full May/June tables.

### Step 4 — Run Part 3 tests

```bash
cd part3_narrative
python -m unittest -v
cd ..
```

The narrative artifacts are Markdown files, and the masking implementation is tested for both the safe and negative raw-name cases.

### Step 5 — Run Part 4 tests

```bash
cd part4_agent
python -m unittest -v
cd ..
```

These tests verify the May and June scenarios, the corrupted-feed Hard Stop, and numeric traceability in drafted messages.

## Run the Part 4 mock agent manually

The runner exposes:

```text
run(month, previous_month_csv, current_month_csv)
```

To execute all three acceptance scenarios with automatically split month-specific feeds:

```bash
python part4_agent/run_examples.py
```

This prints the May valid run, June valid run, and corrupted-current-feed Hard Stop as structured JSON. The lower-level `mock_agent_runner.py` can also be imported and called directly when supplying two month-specific CSV files.

The runner itself does not send email or make network calls. It returns a structured JSON object with `action_taken = "drafted_and_held_for_approval"` for valid runs and `action_taken = "hard_stop"` for invalid runs.

## Acceptance values reproduced

### Part 1

- April Ethnic Wear: INR 104520.77, 64 orders
- May Ethnic Wear: INR 185107.61, 104 orders
- June Ethnic Wear: INR 76371.53, 52 orders
- North: INR 337125.46, 231 orders
- West: INR 333106.33, 232 orders
- South: INR 316736.68, 216 orders
- East: INR 275098.45, 221 orders
- Grand total: INR 1262066.92
- June Delivered AOV: INR 1267.69
- Only zero-order reseller: RS024
- RS024 LEFT JOIN demonstration: `COUNT(*) = 1`, `COUNT(order_id) = 0`

### Part 2

Default threshold: **8.0%**.

- April → May Ethnic Wear: **77.1%**, `flagged`
- May → June Beauty & Personal Care: **5.67%**, `not_flagged`
- 100000 → 108000: **8.0%**, `escalate_exact_boundary`
- Corrupted feed: exactly the three required validation errors
- May: all five categories flagged
- June: four categories flagged; Beauty & Personal Care is not flagged

### Part 4

- May top three drafts: Ethnic Wear 77.1%, Western Wear -23.6%, Kids Wear -23.48%
- May suppressed: Beauty & Personal Care and Home & Kitchen
- June top three drafts: Ethnic Wear -58.74%, Home & Kitchen 42.59%, Kids Wear 23.9%
- June suppressed: Western Wear
- June Beauty & Personal Care 5.67% is neither flagged nor suppressed
- Corrupted current feed: Hard Stop with no MoM computation
- Exact-boundary list is present and empty for the real May/June scenarios

## How the Parts connect

```text
Part 1: SQL computes verified numbers
          ↓
Part 2: validates the feed and computes testable MoM significance
          ↓
Part 3: turns verified values into guarded stakeholder narrative
          ↓
Part 4: orchestrates validation → growth detection → capped drafting → human review
```

The handoff is deliberately sequential. Part 1 is the source of truth for monthly category revenue. Part 2 consumes that output and supplies the deterministic growth status. Part 3 provides the narrative template-fill logic. Part 4 imports the Part 2 functions **unmodified** and calls the Part 3 template-fill function rather than duplicating either implementation.

## Safety and reliability design

1. **No invented figures:** drafted messages receive only verified Part 1/Part 2 values.
2. **Input validation first:** invalid feeds cause a Hard Stop before MoM computation.
3. **Explicit threshold:** absolute MoM change greater than 8% is flagged; less than 8% is not flagged; exactly 8% is escalated for human review.
4. **Notification-flood protection:** only the three largest flagged categories by absolute change are drafted; remaining flagged categories are suppressed for manual review.
5. **Human-in-the-loop:** drafts are held for approval and are never automatically sent.
6. **Privacy:** reseller names are masked as aliases in the external-facing narrative.
7. **Offline operation:** no API key, network request, email integration, or paid service is required.

## Official Python documentation consulted

Implementation uses Python standard-library modules only. Relevant official Python documentation references are:

- `csv` module — CSV reading/writing and `DictReader`.
- `sqlite3` module — SQLite database connections and queries.
- `unittest` module — assertion-based test cases and test discovery.
- `json` module — structured JSON serialization for the mock agent output.
- `os` and `argparse` — portable paths and command-line interfaces.

No external package documentation or paid service was required.

## GitHub submission

After verifying the repository locally, create a **public** GitHub repository and push this folder.

```bash
git init
git add .
git commit -m "Build Meesho reseller growth monitoring pipeline"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/meesho-reseller-growth-pipeline.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username and create the public repository with the matching name before running the final push.

The graded submission should be the resulting **public GitHub repository link only**, as required by the project brief.
