from datetime import date, datetime
import logging
import unittest
from pandas import DataFrame, Series
from unittest.mock import patch, Mock
from .test_data import moving_averages_test_cases, engulfing_candlestick_test_cases, alpaca_can_query_today_closing_price_test_cases, get_first_last_market_days_test_cases
from trade_bot.alpaca_trade_manager import AlpacaTradeManager
from trade_bot.trading import engulfing_candlestick_signal_generator, moving_average_signal_generator, get_first_last_market_days, alpaca_can_query_today_closing_price
from trade_bot.trading import BEARISH, BULLISH, NO_CLEAR_PATTERN


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
    
    @patch('trade_bot.trading.get_first_last_market_days', return_value=("2023-07-25", "2023-07-26"))
    def test_engulfing_candlestick_signal_generator(self, mock_get_first_last_market_days):
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



    @patch('trade_bot.trading.datetime')
    def test_alpaca_can_query_today_closing_price(self, mock_datetime):
        for test_case in alpaca_can_query_today_closing_price_test_cases:
            with self.subTest(msg=test_case["name"]):
                mock_datetime.now.return_value = test_case["now"]
                mock_datetime.strptime.return_value = datetime.strptime("16:16", "%H:%M")
                self.assertEqual(alpaca_can_query_today_closing_price(), test_case["expected"])


    @patch('trade_bot.trading.alpaca_can_query_today_closing_price')
    @patch('trade_bot.trading.date')
    def test_get_first_last_market_days(self, mock_date, mock_alpaca_can_query_today_closing_price):
        for test_case in get_first_last_market_days_test_cases:
            with self.subTest(msg=test_case["name"]):
                mock_date.today.return_value = test_case["date"]
                mock_alpaca_can_query_today_closing_price.return_value = test_case["query_today"]
                start_date, end_date = get_first_last_market_days(test_case["market_days_period"])
                self.assertEqual(start_date, test_case["expected_start_date"])
                self.assertEqual(end_date, test_case["expected_end_date"])


if __name__ == '__main__':
    unittest.main()
