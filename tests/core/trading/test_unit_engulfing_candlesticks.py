import logging
import unittest
from pandas import Series
from unittest.mock import patch
from tests.test_data import engulfing_candlestick_test_cases
from core.trading.engulfing_candlesticks import EngulfingCandlesticks


class TestEngulfingCandleSticks(unittest.TestCase):
    @patch('core.utils.market_time.get_market_day_range', return_value=("2023-07-25", "2023-07-26"))
    def test_engulfing_candlestick_signal_generator(self, mock_get_market_day_range):
        for test_case in engulfing_candlestick_test_cases:
            with self.subTest(msg=test_case["name"]):
                opens = Series([test_case["previous_open"], test_case["open"]])
                closes = Series([test_case["previous_close"], test_case["close"]])
                strat = EngulfingCandlesticks(open_prices=opens,close_prices=closes)
                self.assertEqual(strat.signal(), test_case["expected"])



if __name__ == '__main__':
    unittest.main()
