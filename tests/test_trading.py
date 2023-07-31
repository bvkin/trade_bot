from datetime import datetime
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

    @patch('trade_bot.alpaca_trade_manager.datetime.datetime')
    def test_get_first_last_market_days(self, mock_datetime):
        test_cases = [
            {
                # Spans over week days
                "name": "over_week_market_inactive",
                "date": datetime(2023, 7, 28), # Friday
                "market_days_period": 5,
                "market_active": False,
                "expected_start_date": '2023-07-24',
                "expected_end_date": "2023-07-28"
            },
            {
                # Spans over a weekend
                "name": "over_weekend_market_inactive",
                "date": datetime(2023, 7, 31), # Monday
                "market_days_period": 2,
                "market_active": False,
                "expected_start_date": '2023-07-28',
                "expected_end_date": "2023-07-31"
            },
            {
                # Is weekend
                "name": "is_weekend",
                "date": datetime(2023, 7, 30), # Monday
                "market_days_period": 2,
                "market_active": False,
                "expected_start_date": '2023-07-27',
                "expected_end_date": "2023-07-28"
            },
            {
                # Spans over a holidays
                "name": "over_holiday_market_inactive",
                "date": datetime(2023, 7, 7), # July 7th through July 4th
                "market_days_period": 5,
                "market_active": False,
                "expected_start_date": '2023-06-30',
                "expected_end_date": "2023-07-07"
            },
            {
                # Spans over week days when market is active
                "name": "over_week_market_active",
                "date": datetime(2023, 7, 28), # Friday
                "market_days_period": 4,
                "market_active": True,
                "expected_start_date": '2023-07-24',
                "expected_end_date": "2023-07-27"
            },
            {
                # Spans over a weekend when market is active
                "name": "over_weekend_market_active",
                "date": datetime(2023, 7, 31), # Monday
                "market_days_period": 2,
                "market_active": True,
                "expected_start_date": '2023-07-27',
                "expected_end_date": "2023-07-28"
            },
            {
                # Spans over a holidays market active
                "name": "over_holiday_market_inactive",
                "date": datetime(2023, 7, 7), # July 7th through July 4th
                "market_days_period": 5,
                "market_active": True,
                "expected_start_date": '2023-06-29',
                "expected_end_date": "2023-07-06"
            },
        ]

        for test_case in test_cases:
            with self.subTest(msg=test_case["name"]):
                mock_datetime.now.return_value = test_case["date"]
                start_date, end_date = get_first_last_market_days(test_case["market_days_period"], market_active=test_case["market_active"])
                self.assertEqual(start_date, test_case["expected_start_date"])
                self.assertEqual(end_date, test_case["expected_end_date"])


if __name__ == '__main__':
    unittest.main()
