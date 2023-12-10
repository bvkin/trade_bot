import unittest
from pandas import DataFrame
from tests.test_data import bbands_rsi_test_cases
from core.trading.bbands_rsi import BBandsRSI

class TestBBandsRSI(unittest.TestCase):
    def test_bbands_rsi_signal_generator(self):
        for test_case in bbands_rsi_test_cases:
            with self.subTest(msg=test_case["name"]):
                df = DataFrame({
                    "close": test_case["close_prices"]
                })
                strat = BBandsRSI(df)
                self.assertEqual(strat.signal(), test_case["expected"])

if __name__ == '__main__':
    unittest.main()
