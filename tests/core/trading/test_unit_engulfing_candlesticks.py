import logging
import unittest
from pandas import DataFrame
from unittest.mock import patch
from tests.test_data import engulfing_candlestick_test_cases
from core.trading.engulfing_candlesticks import engulfing_candlestick_signal_generator


class TestEngulfingCandleSticks(unittest.TestCase):
    @patch('core.utils.market_time.get_market_day_range', return_value=("2023-07-25", "2023-07-26"))
    def test_engulfing_candlestick_signal_generator(self, mock_get_market_day_range):
        for test_case in engulfing_candlestick_test_cases:
            with self.subTest(msg=test_case["name"]):
                df = DataFrame(
                    {
                     'open': [test_case["previous_open"], test_case["open"]],
                     'close': [test_case["previous_close"], test_case["close"]]
                    },
                    index=test_case["index"]
                )

                self.assertEqual(engulfing_candlestick_signal_generator(df), test_case["expected"])



if __name__ == '__main__':
    unittest.main()
