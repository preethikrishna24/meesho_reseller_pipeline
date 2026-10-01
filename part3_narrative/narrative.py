"""Deterministic offline narrative template-fill logic used by Part 4."""

PROMPT_TEMPLATE = (
    "Context: {category} revenue is compared for {month} vs. {prev_month}, "
    "from INR {previous_revenue} to INR {current_revenue}.\n"
    "Insight (Fact): {category} changed {mom_pct}% Month-on-Month.\n"
    "Implication (Hypothesis): Review category-level demand, assortment, pricing, "
    "and operational drivers before taking the next action."
)


def fill_prompt_template(
    *, category: str, previous_revenue: float, current_revenue: float,
    mom_pct: float, month: str, prev_month: str
) -> str:
    """Fill the offline narrative template from verified values only."""
    return PROMPT_TEMPLATE.format(
        category=category,
        previous_revenue=previous_revenue,
        current_revenue=current_revenue,
        mom_pct=mom_pct,
        month=month,
        prev_month=prev_month,
    )


def draft_flagged_message(
    *, category: str, previous_revenue: float, current_revenue: float,
    mom_pct: float, month: str, prev_month: str
) -> str:
    """Return the stakeholder-ready draft used by the mock agent."""
    return fill_prompt_template(
        category=category,
        previous_revenue=previous_revenue,
        current_revenue=current_revenue,
        mom_pct=mom_pct,
        month=month,
        prev_month=prev_month,
    )
