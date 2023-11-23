import logging
import unittest
from pandas import DataFrame
from tests.test_data import moving_averages_test_cases
from core.trading.moving_averages import MovingAverages


class TestMovingAverages(unittest.TestCase):
    def test_moving_average_signal_generator(self):
        # Supress WARNING for exception cases
        logging.disable(logging.WARNING)
        
        for test_case in moving_averages_test_cases:
            with self.subTest(msg=f'{test_case["name"]}: {test_case["description"]}'):
                df = DataFrame({"close": test_case["close_prices"]})
                strat = MovingAverages(df)
                self.assertEqual(strat.signal(), test_case["expected"])

        # Re-enable WARNING
        logging.disable(logging.WARNING)


if __name__ == '__main__':
    unittest.main()
