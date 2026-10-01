# Agent Specification

## Goal
Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every drafted message before it is considered sent.

## Tools
- `validate_feed` from Part 2: validates the current and previous monthly revenue feeds before analysis.
- `mom_growth` from Part 2: computes the verified Month-on-Month percentage.
- `is_flagged` from Part 2: classifies the percentage as `flagged`, `not_flagged`, or `escalate_exact_boundary`.
- `draft_flagged_message` / `fill_prompt_template` from Part 3: deterministic offline template-fill logic using verified values only.

## Memory / State
The agent remembers the previous month's verified revenue by category so the next run can compute MoM growth. In the implementation, that state is represented by the previous-month CSV supplied to `run()`; no external database or service is required.

## Planner
1. Load the monthly revenue feeds and run `validate_feed`.
2. If either feed is invalid, Hard Stop and report all validation errors; do not calculate MoM.
3. If valid, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by `abs(mom_pct)` descending.
6. Draft a message via the Part 3 template for at most the top 3 flagged categories by magnitude.
7. Log any remaining flagged categories as `suppressed, review manually`; do not draft them.
7b. Log every `escalate_exact_boundary` category in `escalated_categories`; do not draft it. The exact boundary is neither flagged nor not-flagged.
8. Emit one structured JSON object for the run.

## Feedback Loop
Every drafted message is held for human approval. The mock runner represents this by `action_taken = "drafted_and_held_for_approval"`; it never sends email, makes a network call, or contacts a customer.

## Guardrails

### Input guardrail
`validate_feed` must pass before any growth computation or drafting occurs. Invalid input produces a Hard Stop with the validation errors surfaced.

### Action guardrail
No message is ever auto-sent. Messages are only drafted and held for human review.

### Output guardrail
Every number in a drafted message must trace directly to a verified Part 1/Part 2 value supplied to the template. The template cannot introduce new metrics, invented causes, or raw reseller names.

## Success and Error Stopping Conditions
**Success:** Drafts are produced for flagged categories, or correctly zero drafts are produced when nothing crosses the threshold. Every emitted number is traceable to verified input, and exact-boundary categories are separately escalated.

**Error:** `validate_feed` returns `False`. The run becomes a Hard Stop, validation errors are surfaced, and `flagged_categories` and `suppressed_categories` remain empty. No MoM computation is attempted on invalid data.

## Structured Output Contract
Every run returns exactly these top-level keys:

- `run_month`
- `validation_status` — `valid` or `invalid`
- `validation_errors` — list, empty on success
- `flagged_categories` — objects containing `category`, `mom_pct`, `previous_revenue`, `current_revenue`, `drafted`, and `message` when drafted
- `suppressed_categories` — category names that were flagged but exceeded the top-3 draft cap
- `escalated_categories` — categories exactly on the 8.0% boundary
- `action_taken` — `drafted_and_held_for_approval` or `hard_stop`

## Agent-Level Given-When-Then Specifications

### 1. April → May Ethnic Wear
**GIVEN** April → May Ethnic Wear revenue moves from 104520.77 to 185107.61, **WHEN** `mom_growth` then `is_flagged` run on it, **THEN** `mom_growth` returns 77.1 and `is_flagged` returns `"flagged"`.

### 2. May → June Beauty & Personal Care
**GIVEN** May → June Beauty & Personal Care revenue moves from 35542.11 to 37559.07, **WHEN** evaluated, **THEN** `mom_growth` returns 5.67 and `is_flagged` returns `"not_flagged"`.

### 3. Exact boundary
**GIVEN** a synthetic pair previous=100000, current=108000, **WHEN** evaluated, **THEN** `mom_growth` returns exactly 8.0 and `is_flagged` returns `"escalate_exact_boundary"` — not `"flagged"` and not `"not_flagged"`.

### 4. Corrupted feed
**GIVEN** the corrupted feed fixture, **WHEN** `validate_feed` runs, **THEN** it returns `(False, errors)` where `errors` has exactly 3 entries, matching in order: the negative-revenue row, the missing-category row, and the missing-revenue row.
