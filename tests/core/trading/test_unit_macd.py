import logging
import unittest
from pandas import DataFrame
from tests.test_data import macd_test_cases
from core.trading.macd import MACD


class TestMACD(unittest.TestCase):
    def test_moving_average_signal_generator(self):
        for test_case in macd_test_cases:
            with self.subTest(msg=f'{test_case["name"]}: {test_case["description"]}'):
                df = DataFrame({"close": test_case["close_prices"]})
                strat = MACD(df)
                self.assertEqual(strat.signal(), test_case["expected"])

        # Re-enable WARNING
        logging.disable(logging.WARNING)


if __name__ == '__main__':
    unittest.main()
