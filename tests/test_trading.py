import datetime
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
                "open": 13,
                "close": 6,
                "previous_open": 7,
                "previous_close": 8,
                "index": ["2023-07-25", "2023-07-26"],
                "expected": 1
            },
            {
                "name": "bullish",
                "open": 10,
                "close": 13,
                "previous_open": 12,
                "previous_close": 11,
                "index": ["2023-07-25", "2023-07-26"],
                "expected": 2
            },
            {
                "name": "no clear pattern",
                "open": 11,
                "close": 12,
                "previous_open": 10,
                "previous_close": 11,
                "index": ["2023-07-25", "2023-07-26"],
                "expected": 0
            }
        ]

        for test_case in test_cases:
            with self.subTest(msg=test_case["name"]):
                self.trade_manager.get_price_data.return_value = DataFrame(
                    {
                     'open': [test_case["previous_open"], test_case["open"]],
                     'close': [test_case["previous_close"], test_case["close"]]
                    },
                    index=test_case["index"]
                )

                self.assertEqual(engulfing_candlestick_signal_generator(self.trade_manager, "TEST"), test_case["expected"])


if __name__ == '__main__':
    unittest.main()
