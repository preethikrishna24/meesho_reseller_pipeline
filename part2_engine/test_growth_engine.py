"""Given-When-Then tests for the Part 2 growth engine."""
import os
import unittest

from growth_engine import is_flagged, mom_growth, validate_feed

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")


class TestGrowthEngine(unittest.TestCase):
    def test_april_to_may_ethnic_wear_is_flagged(self):
        # GIVEN April -> May Ethnic Wear revenue moves from 104520.77 to 185107.61
        # WHEN mom_growth and is_flagged are run
        # THEN growth is 77.1 and the category is flagged
        growth = mom_growth(104520.77, 185107.61)
        self.assertEqual(growth, 77.1)
        self.assertEqual(is_flagged(growth), "flagged")

    def test_may_to_june_beauty_is_not_flagged(self):
        # GIVEN May -> June Beauty & Personal Care revenue moves from 35542.11 to 37559.07
        # WHEN evaluated
        # THEN growth is 5.67 and it is not flagged
        growth = mom_growth(35542.11, 37559.07)
        self.assertEqual(growth, 5.67)
        self.assertEqual(is_flagged(growth), "not_flagged")

    def test_exact_boundary_escalates(self):
        # GIVEN previous=100000 and current=108000
        # WHEN evaluated at the default 8% threshold
        # THEN exactly 8.0 escalates for human review
        growth = mom_growth(100000, 108000)
        self.assertEqual(growth, 8.0)
        self.assertEqual(is_flagged(growth), "escalate_exact_boundary")

    def test_corrupted_feed_returns_exact_errors(self):
        # GIVEN the corrupted feed fixture
        # WHEN validate_feed runs
        # THEN exactly the three expected errors are returned in order
        ok, errors = validate_feed(os.path.join(FIXTURES, "corrupted_feed.csv"))
        self.assertFalse(ok)
        self.assertEqual(errors, [
            "line 3: negative revenue (-4200.0) for category=Western Wear",
            "line 4: missing category (month=July)",
            "line 6: missing revenue (category=Home & Kitchen)",
        ])

    def test_valid_part1_feed_passes(self):
        ok, errors = validate_feed(os.path.join(FIXTURES, "monthly_category_revenue.csv"))
        self.assertTrue(ok)
        self.assertEqual(errors, [])

    def test_may_table(self):
        expected = {
            "Ethnic Wear": (77.1, "flagged"),
            "Western Wear": (-23.6, "flagged"),
            "Kids Wear": (-23.48, "flagged"),
            "Home & Kitchen": (-9.25, "flagged"),
            "Beauty & Personal Care": (-12.75, "flagged"),
        }
        for category, (expected_pct, expected_status) in expected.items():
            # Values are from the seeded Part 1 acceptance output.
            import csv
            with open(os.path.join(FIXTURES, "monthly_category_revenue.csv"), newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            values = {r["month"] + "|" + r["category"]: float(r["revenue"]) for r in rows}
            pct = mom_growth(values["April|" + category], values["May|" + category])
            self.assertEqual(pct, expected_pct)
            self.assertEqual(is_flagged(pct), expected_status)

    def test_june_table(self):
        expected = {
            "Ethnic Wear": (-58.74, "flagged"),
            "Western Wear": (11.97, "flagged"),
            "Kids Wear": (23.9, "flagged"),
            "Home & Kitchen": (42.59, "flagged"),
            "Beauty & Personal Care": (5.67, "not_flagged"),
        }
        import csv
        with open(os.path.join(FIXTURES, "monthly_category_revenue.csv"), newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        values = {r["month"] + "|" + r["category"]: float(r["revenue"]) for r in rows}
        for category, (expected_pct, expected_status) in expected.items():
            pct = mom_growth(values["May|" + category], values["June|" + category])
            self.assertEqual(pct, expected_pct)
            self.assertEqual(is_flagged(pct), expected_status)


if __name__ == "__main__":
    unittest.main()
