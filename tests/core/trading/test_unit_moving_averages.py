import logging
import unittest
from pandas import Series
from tests.test_data import moving_averages_test_cases
from core.trading.moving_averages import moving_average_signal_generator


class TestMovingAverages(unittest.TestCase):
    def test_moving_average_signal_generator(self):
        # Supress WARNING for exception cases
        logging.disable(logging.WARNING)

        for test_case in moving_averages_test_cases:
            with self.subTest(msg=f'{test_case["name"]}: {test_case["description"]}'):
                closes = Series(test_case["close_prices"])
                self.assertEqual(moving_average_signal_generator(closes), test_case["expected"])

        # Re-enable WARNING
        logging.disable(logging.WARNING)


if __name__ == '__main__':
    unittest.main()