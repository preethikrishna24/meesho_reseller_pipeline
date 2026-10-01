import csv
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PART2_FIXTURES = os.path.join(ROOT, "part2_engine", "fixtures")
PART1_OUTPUT = os.path.join(ROOT, "part1_sql", "output", "monthly_category_revenue.csv")
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from mock_agent_runner import run


class TestMockAgentRunner(unittest.TestCase):
    def setUp(self):
        with open(PART1_OUTPUT, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.april = os.path.join(HERE, "_test_april.csv")
        self.may = os.path.join(HERE, "_test_may.csv")
        self.june = os.path.join(HERE, "_test_june.csv")
        for month, path in [("April", self.april), ("May", self.may), ("June", self.june)]:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["month", "category", "revenue", "n_orders"])
                writer.writeheader()
                writer.writerows(r for r in rows if r["month"] == month)

    def tearDown(self):
        for path in [self.april, self.may, self.june]:
            if os.path.exists(path):
                os.remove(path)

    def test_may_scenario(self):
        result = run("May", self.april, self.may)
        self.assertEqual(result["validation_status"], "valid")
        self.assertEqual([(x["category"], x["mom_pct"]) for x in result["flagged_categories"]], [
            ("Ethnic Wear", 77.1), ("Western Wear", -23.6), ("Kids Wear", -23.48)
        ])
        self.assertEqual(set(result["suppressed_categories"]), {"Beauty & Personal Care", "Home & Kitchen"})
        self.assertEqual(result["escalated_categories"], [])
        self.assertTrue(all(x["drafted"] for x in result["flagged_categories"]))
        self.assertEqual(result["action_taken"], "drafted_and_held_for_approval")

    def test_june_scenario(self):
        result = run("June", self.may, self.june)
        self.assertEqual(result["validation_status"], "valid")
        self.assertEqual([(x["category"], x["mom_pct"]) for x in result["flagged_categories"]], [
            ("Ethnic Wear", -58.74), ("Home & Kitchen", 42.59), ("Kids Wear", 23.9)
        ])
        self.assertEqual(result["suppressed_categories"], ["Western Wear"])
        self.assertEqual(result["escalated_categories"], [])
        self.assertNotIn("Beauty & Personal Care", result["suppressed_categories"])

    def test_corrupted_feed_hard_stop(self):
        result = run("July", self.may, os.path.join(PART2_FIXTURES, "corrupted_feed.csv"))
        self.assertEqual(result["validation_status"], "invalid")
        self.assertEqual(result["action_taken"], "hard_stop")
        self.assertEqual(result["validation_errors"], [
            "line 3: negative revenue (-4200.0) for category=Western Wear",
            "line 4: missing category (month=July)",
            "line 6: missing revenue (category=Home & Kitchen)",
        ])
        self.assertEqual(result["flagged_categories"], [])
        self.assertEqual(result["suppressed_categories"], [])

    def test_message_traceability_shape(self):
        result = run("May", self.april, self.may)
        for item in result["flagged_categories"]:
            message = item["message"]
            self.assertIn(item["category"], message)
            self.assertIn(str(item["mom_pct"]), message)
            self.assertIn(str(item["previous_revenue"]), message)
            self.assertIn(str(item["current_revenue"]), message)


if __name__ == "__main__":
    unittest.main()
