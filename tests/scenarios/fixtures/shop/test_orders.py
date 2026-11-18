import unittest
from datetime import date, timedelta

from orders import RETURN_WINDOW_DAYS, Order, OrderStatus, can_return


class CanReturnTest(unittest.TestCase):
    def test_delivered_on_last_allowed_day_returns_true(self):
        order = Order(
            status=OrderStatus.DELIVERED,
            delivered_on=date(2026, 1, 1),
        )
        today = date(2026, 1, 1) + timedelta(days=RETURN_WINDOW_DAYS)
        self.assertTrue(can_return(order, today))

    def test_delivered_one_day_past_window_returns_false(self):
        order = Order(
            status=OrderStatus.DELIVERED,
            delivered_on=date(2026, 1, 1),
        )
        today = date(2026, 1, 1) + timedelta(days=RETURN_WINDOW_DAYS + 1)
        self.assertFalse(can_return(order, today))


if __name__ == "__main__":
    unittest.main()
