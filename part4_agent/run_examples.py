"""Convenience helper to run the acceptance scenarios from the integrated output."""
import csv
import json
import os
import tempfile

from mock_agent_runner import run

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "part1_sql", "output", "monthly_category_revenue.csv")
CORRUPTED = os.path.join(ROOT, "part2_engine", "fixtures", "corrupted_feed.csv")


def split_months():
    with open(SOURCE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    paths = {}
    for month in ("April", "May", "June"):
        fd, path = tempfile.mkstemp(prefix=f"{month.lower()}_", suffix=".csv")
        os.close(fd)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["month", "category", "revenue", "n_orders"])
            writer.writeheader()
            writer.writerows(row for row in rows if row["month"] == month)
        paths[month] = path
    return paths


def main():
    paths = split_months()
    try:
        print("MAY")
        print(json.dumps(run("May", paths["April"], paths["May"]), indent=2))
        print("JUNE")
        print(json.dumps(run("June", paths["May"], paths["June"]), indent=2))
        print("CORRUPTED")
        print(json.dumps(run("July", paths["June"], CORRUPTED), indent=2))
    finally:
        for path in paths.values():
            os.remove(path)


if __name__ == "__main__":
    main()
