# Reusable Prompt Pack — Flagged Category Update

## Trigger
A category's `is_flagged` result is exactly `"flagged"`, meaning the absolute Month-on-Month revenue change is greater than the 8.0% threshold.

## Input list
- `{category}` — category name.
- `{previous_revenue}` — verified revenue for the prior month.
- `{current_revenue}` — verified revenue for the current month.
- `{mom_pct}` — verified MoM percentage from `mom_growth`.
- `{month}` — current month name.
- `{prev_month}` — prior month name, used to name the comparison explicitly (for example, “May vs. April”).

## Prompt
Using only the supplied verified placeholders, write a concise stakeholder update for a regional/category manager in **Context → Insight → Implication** order.

**Context:** State that `{category}` revenue is being compared for `{month}` versus `{prev_month}` and identify the supplied revenue values `{previous_revenue}` and `{current_revenue}`.

**Insight:** State `{mom_pct}%` exactly as supplied and label it explicitly as a **Fact**. Do not calculate, round, infer, or introduce any number other than the supplied placeholders.

**Implication:** Give one concrete next action appropriate for a manager. If you propose a possible cause that the supplied data does not prove, label it explicitly as a **Hypothesis** rather than stating it as fact.

Do not state any number that is not one of `{previous_revenue}`, `{current_revenue}`, `{mom_pct}`, or a number explicitly present in the supplied context. Do not invent reseller names, order counts, targets, causes, or other metrics. Keep the update concise and decision-oriented.

## Checklist
1. **Numeric traceability:** Does every number in the draft exactly match one of the supplied numeric placeholder values?
2. **Fact/hypothesis separation:** Is each data-backed observation labeled **Fact**, and is every unproven cause labeled **Hypothesis**?
3. **Specificity:** Are the category and both month names stated correctly, with the exact supplied MoM percentage?
4. **Actionability:** Does the implication contain a concrete next step rather than a vague instruction such as “look into it”?
5. **Audience fit:** Is the language written for a stakeholder/manager rather than a data engineer?
6. **Privacy/masking:** If a reseller is referenced, is it represented only by a coded alias and never by its raw reseller name?
