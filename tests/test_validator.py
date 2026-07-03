import unittest
from validator import validate_required, validate_customer_id, validate_date


class TestValidateRequired(unittest.TestCase):
    def test_valid_input(self):
        self.assertIsNone(validate_required("hello", "필드"))

    def test_empty_string(self):
        self.assertIsNotNone(validate_required("", "필드"))

    def test_whitespace_only(self):
        self.assertIsNotNone(validate_required("   ", "필드"))

    def test_none_value(self):
        self.assertIsNotNone(validate_required(None, "필드"))


class TestValidateCustomerId(unittest.TestCase):
    def test_valid_c001(self):
        self.assertIsNone(validate_customer_id("C001"))

    def test_valid_c999(self):
        self.assertIsNone(validate_customer_id("C999"))

    def test_lowercase_c(self):
        self.assertIsNotNone(validate_customer_id("c001"))

    def test_missing_prefix(self):
        self.assertIsNotNone(validate_customer_id("001"))

    def test_too_short_number(self):
        self.assertIsNotNone(validate_customer_id("C01"))

    def test_too_long_number(self):
        self.assertIsNotNone(validate_customer_id("C0001"))

    def test_non_numeric_suffix(self):
        self.assertIsNotNone(validate_customer_id("Cabc"))


class TestValidateDate(unittest.TestCase):
    def test_valid_date(self):
        self.assertIsNone(validate_date("2026-06-09"))

    def test_valid_date_feb_28(self):
        self.assertIsNone(validate_date("2026-02-28"))

    def test_invalid_format_no_dash(self):
        self.assertIsNotNone(validate_date("20260609"))

    def test_invalid_format_wrong_separator(self):
        self.assertIsNotNone(validate_date("2026/06/09"))

    def test_nonexistent_date_feb_30(self):
        self.assertIsNotNone(validate_date("2026-02-30"))

    def test_nonexistent_date_apr_31(self):
        self.assertIsNotNone(validate_date("2026-04-31"))

    def test_invalid_month(self):
        self.assertIsNotNone(validate_date("2026-13-01"))

    def test_invalid_day(self):
        self.assertIsNotNone(validate_date("2026-01-32"))

    def test_empty_string(self):
        self.assertIsNotNone(validate_date(""))

    def test_leap_year_feb_29_2024(self):
        self.assertIsNone(validate_date("2024-02-29"))

    def test_non_leap_year_feb_29_2025(self):
        self.assertIsNotNone(validate_date("2025-02-29"))


if __name__ == "__main__":
    unittest.main()