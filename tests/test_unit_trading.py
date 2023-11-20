import logging
import unittest
from pandas import DataFrame, Series
from unittest.mock import patch, Mock
from tests.test_data import moving_averages_test_cases, engulfing_candlestick_test_cases
from core.alpaca.alpaca_trade_manager import AlpacaTradeManager
from trade_bot.trading import engulfing_candlestick_signal_generator, moving_average_signal_generator


class TestTrading(unittest.TestCase):
    def setUp(self):
        self.trade_manager = AlpacaTradeManager("api_key", "secret_key")
        self.trade_manager.get_price_data = Mock()

    def test_moving_average_signal_generator(self):
        # Supress WARNING for exception cases
        logging.disable(logging.WARNING)

        for test_case in moving_averages_test_cases:
            with self.subTest(msg=f'{test_case["name"]}: {test_case["description"]}'):
                closes = Series(test_case["close_prices"])
                self.assertEqual(moving_average_signal_generator(closes), test_case["expected"])

        # Re-enable WARNING
        logging.disable(logging.WARNING)
    
    @patch('trade_bot.trading.get_market_day_range', return_value=("2023-07-25", "2023-07-26"))
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
