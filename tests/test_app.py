import unittest
from datetime import date

from app import app, calculate_age


class AgeCalculatorTests(unittest.TestCase):
    def test_age_before_birthday_this_year(self):
        result = calculate_age(date(2000, 12, 31), date(2024, 12, 30))
        self.assertEqual((result["years"], result["months"], result["days"]), (23, 11, 30))

    def test_age_on_leap_day_birthday_in_non_leap_year(self):
        result = calculate_age(date(2000, 2, 29), date(2023, 2, 28))
        self.assertEqual((result["years"], result["months"], result["days"]), (23, 0, 0))
        self.assertEqual(result["days_until_birthday"], 0)

    def test_future_birth_date_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_age(date(2025, 1, 1), date(2024, 12, 31))

    def test_api_returns_calculated_age(self):
        client = app.test_client()
        response = client.post("/api/calculate", json={"birth_date": "2000-01-01"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_days", response.get_json())

    def test_api_rejects_invalid_date(self):
        client = app.test_client()
        response = client.post("/api/calculate", json={"birth_date": "not-a-date"})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()