import unittest
from pandas import DataFrame
from tests.test_data import engulfing_candlestick_test_cases
from core.trading.engulfing_candlesticks import EngulfingCandlesticks


class TestEngulfingCandleSticks(unittest.TestCase):
    def test_engulfing_candlestick_signal_generator(self):
        for test_case in engulfing_candlestick_test_cases:
            with self.subTest(msg=test_case["name"]):
                # talib needs three values to give a signal
                df = DataFrame({
                    "open" : [100, test_case["prev_open"], test_case["open"]],
                    "high" : [100, test_case["prev_high"], test_case["high"]],
                    "low"  : [100, test_case["prev_low"], test_case["low"]],
                    "close": [100, test_case["prev_close"], test_case["close"]]
                })

                strat = EngulfingCandlesticks(df)
                self.assertEqual(strat.signal(), test_case["expected"])



if __name__ == '__main__':
    unittest.main()
