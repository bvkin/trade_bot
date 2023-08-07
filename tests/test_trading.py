from datetime import date, datetime
import logging
import unittest
from pandas import DataFrame
import pytz
from unittest.mock import patch, Mock
from trade_bot.alpaca_trade_manager import AlpacaTradeManager
from trade_bot.trading import engulfing_candlestick_signal_generator, moving_average_singnal_generator, get_first_last_market_days, is_after_alpaca_market_hours
from trade_bot.trading import BEARISH, BULLISH, NO_CLEAR_PATTERN


class TestTrading(unittest.TestCase):
    def setUp(self):
        self.trade_manager = AlpacaTradeManager("api_key", "secret_key")
        self.trade_manager.get_price_data = Mock()

    def test_moving_average_singnal_generator(self):
        test_cases = [
            {
                "name": "bullish",
                "description": "5_day_ma == 117, 20_day_ma == 109.5",
                "close_prices": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119],
                "expected": BULLISH
            },
            {
                "name": "bearish",
                "description": "5_day_ma == 103, 20_day_ma == 110.5",
                "close_prices": [120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101],
                "expected": BEARISH
            },
            {
                "name": "bearish",
                "description": "5_day_ma == 100, 20_day_ma == 100",
                "close_prices": [100] * 20,
                "expected": NO_CLEAR_PATTERN
            },
            {
                "name": "index_error",
                "description": "trigger index out of bounds exception",
                "close_prices": [100] * 4,
                "expected": NO_CLEAR_PATTERN
            }
        ]

        # Supress WARNING for exception cases
        logging.disable(logging.WARNING)

        for test_case in test_cases:
            with self.subTest(msg=f'{test_case["name"]}: {test_case["description"]}'):
                self.trade_manager.get_price_data.return_value = DataFrame({"close" : test_case["close_prices"]})
                self.assertEqual(moving_average_singnal_generator(self.trade_manager, "TEST"), test_case["expected"])

        # Re-enable WARNING
        logging.disable(logging.WARNING)
    
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



    @patch('trade_bot.trading.datetime')
    def test_is_after_alpaca_market_hours(self, mock_datetime):
        eastern = pytz.timezone('US/Eastern')
        test_cases = [
            {
                "name": "after_hours",
                "now": datetime(2023, 7, 27, 17, 31, tzinfo=eastern), # 5:31 PM Eastern
                "expected": True,
            },
            {
                "name": "during_hours",
                "now": datetime(2023, 7, 27, 10, 0, tzinfo=eastern), # 10 AM Eastern
                "expected": False,
            },
            {
                "name": "before_hours",
                "now": datetime(2023, 7, 27, 6, 0, tzinfo=eastern), # 10 AM Eastern
                "expected": False,
            }
        ]

        for test_case in test_cases:
            with self.subTest(msg=test_case["name"]):
                mock_datetime.now.return_value = test_case["now"]
                mock_datetime.strptime.return_value = datetime.strptime("16:16", "%H:%M")
                self.assertEqual(is_after_alpaca_market_hours(), test_case["expected"])


    @patch('trade_bot.trading.date')
    def test_get_first_last_market_days(self, mock_date):
        test_cases = [
            {
                # Spans over week days
                "name": "over_week_dont_query_today",
                "date": date(2023, 7, 28), # Friday
                "market_days_period": 5,
                "query_today": False,
                "expected_start_date": '2023-07-21',
                "expected_end_date": "2023-07-27"
            },
            {
                # Spans over week days
                "name": "over_week_query_today",
                "date": date(2023, 7, 28), # Friday
                "market_days_period": 5,
                "query_today": True,
                "expected_start_date": '2023-07-24',
                "expected_end_date": "2023-07-28T16:30:00-04:00"
            },
            {
                # Spans over a weekend
                "name": "over_weekend_query_today",
                "date": date(2023, 7, 31), # Monday
                "market_days_period": 2,
                "query_today": True,
                "expected_start_date": '2023-07-28',
                "expected_end_date": "2023-07-31T16:30:00-04:00"
            },
            {
                # Spans over a weekend
                "name": "over_weekend_dont_query_today",
                "date": date(2023, 7, 31), # Monday
                "market_days_period": 2,
                "query_today": False,
                "expected_start_date": '2023-07-27',
                "expected_end_date": "2023-07-28"
            },
            {
                # Is weekend
                "name": "is_weekend_query_today",
                "date": date(2023, 7, 30), # Monday
                "market_days_period": 2,
                "query_today": True,
                "expected_start_date": '2023-07-27',
                "expected_end_date": "2023-07-28"
            },
            {
                # Is weekend
                "name": "is_weekend_dont_query_today",
                "date": date(2023, 7, 30), # Monday
                "market_days_period": 2,
                "query_today": False,
                "expected_start_date": '2023-07-27',
                "expected_end_date": "2023-07-28"
            },
            {
                # Spans over a holidays
                "name": "over_holiday_dont_query_today",
                "date": date(2023, 7, 7), # July 7th through July 4th
                "market_days_period": 5,
                "query_today": False,
                "expected_start_date": '2023-06-29',
                "expected_end_date": "2023-07-06"
            },
            {
                # Spans over a holidays
                "name": "over_holiday_query_today",
                "date": date(2023, 7, 7), # July 7th through July 4th
                "market_days_period": 5,
                "query_today": True,
                "expected_start_date": '2023-06-30',
                "expected_end_date": "2023-07-07T16:30:00-04:00"
            },
        ]

        for test_case in test_cases:
            with self.subTest(msg=test_case["name"]):
                mock_date.today.return_value = test_case["date"]
                start_date, end_date = get_first_last_market_days(test_case["market_days_period"], query_today=test_case["query_today"])
                self.assertEqual(start_date, test_case["expected_start_date"])
                self.assertEqual(end_date, test_case["expected_end_date"])


if __name__ == '__main__':
    unittest.main()
