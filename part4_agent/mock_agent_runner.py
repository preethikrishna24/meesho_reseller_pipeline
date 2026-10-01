"""Offline, human-reviewed mock agent runner for Parts 1-4."""
from __future__ import annotations

import csv
import json
import os
import sys
from typing import Dict, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PART2 = os.path.join(ROOT, "part2_engine")
PART3 = os.path.join(ROOT, "part3_narrative")
if PART2 not in sys.path:
    sys.path.insert(0, PART2)
if PART3 not in sys.path:
    sys.path.insert(0, PART3)

from growth_engine import is_flagged, mom_growth, validate_feed  # noqa: E402
from narrative import draft_flagged_message  # noqa: E402


def _load_feed(path: str) -> Dict[str, float]:
    with open(path, newline="", encoding="utf-8") as f:
        return {row["category"]: float(row["revenue"]) for row in csv.DictReader(f)}


def _hard_stop(errors: List[str]) -> dict:
    return {
        "run_month": None,
        "validation_status": "invalid",
        "validation_errors": errors,
        "flagged_categories": [],
        "suppressed_categories": [],
        "escalated_categories": [],
        "action_taken": "hard_stop",
    }


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """Execute the guarded monitoring flow and return exactly the required schema."""
    valid_previous, previous_errors = validate_feed(previous_month_csv)
    valid_current, current_errors = validate_feed(current_month_csv)
    errors = previous_errors + current_errors
    if not valid_previous or not valid_current:
        result = _hard_stop(errors)
        result["run_month"] = month
        return result

    previous = _load_feed(previous_month_csv)
    current = _load_feed(current_month_csv)

    flagged = []
    suppressed: List[str] = []
    escalated: List[str] = []

    for category, current_revenue in current.items():
        if category not in previous:
            raise ValueError(f"category missing from previous feed: {category}")
        previous_revenue = previous[category]
        pct = mom_growth(previous_revenue, current_revenue)
        status = is_flagged(pct)
        item = {
            "category": category,
            "mom_pct": pct,
            "previous_revenue": previous_revenue,
            "current_revenue": current_revenue,
        }
        if status == "flagged":
            flagged.append(item)
        elif status == "escalate_exact_boundary":
            escalated.append(category)

    flagged.sort(key=lambda item: abs(item["mom_pct"]), reverse=True)
    selected = flagged[:3]
    suppressed = [item["category"] for item in flagged[3:]]

    output_flagged = []
    for item in selected:
        message = draft_flagged_message(
            category=item["category"],
            previous_revenue=item["previous_revenue"],
            current_revenue=item["current_revenue"],
            mom_pct=item["mom_pct"],
            month=month,
            prev_month=_previous_month_name(month),
        )
        output_flagged.append({
            **item,
            "drafted": True,
            "message": message,
        })

    # Suppressed categories are logged but deliberately have no draft/message.
    # Exact-boundary categories are escalated separately and never drafted.
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": output_flagged,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }


def _previous_month_name(month: str) -> str:
    order = {"April": "March", "May": "April", "June": "May", "July": "June"}
    return order.get(month, "previous month")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run the offline Meesho monitoring agent.")
    parser.add_argument("month")
    parser.add_argument("previous_month_csv")
    parser.add_argument("current_month_csv")
    args = parser.parse_args()
    print(json.dumps(run(args.month, args.previous_month_csv, args.current_month_csv), indent=2))


if __name__ == "__main__":
    main()
