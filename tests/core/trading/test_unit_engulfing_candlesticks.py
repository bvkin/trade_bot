import unittest
from pandas import Series
from tests.test_data import engulfing_candlestick_test_cases
from core.trading.engulfing_candlesticks import EngulfingCandlesticks


class TestEngulfingCandleSticks(unittest.TestCase):
    def test_engulfing_candlestick_signal_generator(self):
        for test_case in engulfing_candlestick_test_cases:
            with self.subTest(msg=test_case["name"]):
                # talib needs three values to give a signal
                opens = Series([100, test_case["prev_open"], test_case["open"]])
                closes = Series([100, test_case["prev_close"], test_case["close"]])
                highs = Series([100, test_case["prev_high"], test_case["high"]])
                lows = Series([100, test_case["prev_low"], test_case["low"]])

                strat = EngulfingCandlesticks(
                    open_prices=opens, 
                    high_prices=highs,
                    low_prices=lows,
                    close_prices=closes
                )
                self.assertEqual(strat.signal(), test_case["expected"])



if __name__ == '__main__':
    unittest.main()
