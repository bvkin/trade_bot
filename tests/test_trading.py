import unittest
from pandas import DataFrame
from unittest.mock import patch, Mock
from trade_bot.alpaca_trade_manager import AlpacaTradeManager
from trade_bot.trading import engulfing_candlestick_signal_generator, get_first_last_market_days


class TestTrading(unittest.TestCase):
    def setUp(self):
        self.trade_manager = AlpacaTradeManager("api_key", "secret_key")
        self.trade_manager.get_price_data = Mock()

    @patch('trade_bot.trading.get_first_last_market_days', return_value=("2023-07-25", "2023-07-26"))
    def test_engulfing_candlestick_signal_generator(self, mock_get_first_last_market_days):
        test_cases = [
            {
                "name": "bearish",
                "data": DataFrame({'open': [7, 13], 'close': [8, 6]}, index=["2023-07-25", "2023-07-26"]),
                "expected": 1
            },
            {
                "name": "bullish",
                "data": DataFrame({'open': [12, 10], 'close': [11, 13]}, index=["2023-07-25", "2023-07-26"]),
                "expected": 2
            },
            {
                "name": "no clear pattern",
                "data": DataFrame({'open': [10, 11], 'close': [11, 12]}, index=["2023-07-25", "2023-07-26"]),
                "expected": 0
            }
        ]

        for test_case in test_cases:
            with self.subTest(msg=test_case["name"]):
                self.trade_manager.get_price_data.return_value = test_case["data"]

                self.assertEqual(engulfing_candlestick_signal_generator(self.trade_manager, "TEST"), test_case["expected"])


if __name__ == '__main__':
    unittest.main()
