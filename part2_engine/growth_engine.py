"""Validated growth-detection functions used by Parts 2 and 4."""
import csv


def mom_growth(previous: float, current: float) -> float:
    """Return Month-on-Month percentage growth rounded to two decimals."""
    if previous == 0:
        raise ValueError("previous revenue must not be zero")
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """Classify a MoM percentage with an explicit exact-boundary state."""
    magnitude = abs(mom_pct)
    if magnitude > threshold:
        return "flagged"
    if magnitude < threshold:
        return "not_flagged"
    return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    """Validate the required monthly/category/revenue/n_orders CSV fields."""
    errors: list[str] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_number, row in enumerate(reader, start=2):
            month = row.get("month", "")
            category = row.get("category", "")
            revenue = row.get("revenue", "")

            if category == "":
                errors.append(f"line {line_number}: missing category (month={month})")
            if revenue == "":
                errors.append(f"line {line_number}: missing revenue (category={category})")
            elif _is_non_numeric(revenue):
                errors.append(f"line {line_number}: revenue not numeric: {revenue!r}")
            else:
                value = float(revenue)
                if value < 0:
                    errors.append(f"line {line_number}: negative revenue ({value}) for category={category}")
    return (len(errors) == 0, errors)


def _is_non_numeric(value: str) -> bool:
    try:
        float(value)
    except (TypeError, ValueError):
        return True
    return False
