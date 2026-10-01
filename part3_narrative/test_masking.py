import unittest

from masking import alias_for, assert_no_raw_names_leak


class TestMasking(unittest.TestCase):
    def test_alias(self):
        self.assertEqual(alias_for("RS019"), "ALIAS-19")
        self.assertEqual(alias_for("RS006"), "ALIAS-06")

    def test_no_raw_names_leak(self):
        names = [
            "Mumbai Reseller 1", "Mumbai Reseller 4", "Hyderabad Reseller 6",
            "Lucknow Reseller 6", "Jaipur Reseller 5",
        ]
        safe = "West ALIAS-19 and West ALIAS-22 are coded resellers."
        self.assertTrue(assert_no_raw_names_leak(safe, names))
        unsafe = "West Mumbai Reseller 1 is referenced here."
        self.assertFalse(assert_no_raw_names_leak(unsafe, names))


if __name__ == "__main__":
    unittest.main()
