import unittest
from src.user_service import register_user, calculate_discount, calculate_discount_amount

class TestUserService(unittest.TestCase):
    def test_baseline_registration(self):
        user = register_user('john_doe', 'john@example.com')
        self.assertEqual(user['role'], 'customer')

    def test_baseline_discount(self):
        res = calculate_discount(100.0, 'VIP')
        self.assertEqual(res, 80.0)

    def test_percentage_discount_rounding_15_percent(self):
        discount_amt = calculate_discount_amount(10.00, 15.0)
        self.assertEqual(discount_amt, 1.50)

    def test_percentage_discount_rounding_non_terminating(self):
        discount_amt = calculate_discount_amount(9.99, 33.0)
        self.assertEqual(discount_amt, 3.30)

    def test_negative_order_total_raises_error(self):
        with self.assertRaises(ValueError):
            calculate_discount_amount(-50.0, 15.0)

    def test_vip_and_regular_tier_discounts(self):
        self.assertEqual(calculate_discount(100.0, 'VIP'), 80.0)
        self.assertEqual(calculate_discount(100.0, 'REGULAR'), 95.0)

if __name__ == '__main__':
    unittest.main()
