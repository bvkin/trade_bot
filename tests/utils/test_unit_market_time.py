from datetime import datetime
import unittest
from unittest.mock import patch
from core.utils.market_time import get_market_day_range, alpaca_can_query_today_closing_price
from tests.test_data import get_market_day_range_test_cases, alpaca_can_query_today_closing_price_test_cases

class TestMarketUtils(unittest.TestCase):
    @patch('core.utils.market_time.datetime')
    def test_alpaca_can_query_today_closing_price(self, mock_datetime):
        for test_case in alpaca_can_query_today_closing_price_test_cases:
            with self.subTest(msg=test_case["name"]):
                mock_datetime.now.return_value = test_case["now"]
                mock_datetime.strptime.return_value = datetime.strptime("16:16", "%H:%M")
                self.assertEqual(alpaca_can_query_today_closing_price(), test_case["expected"])


    @patch('core.utils.market_time.alpaca_can_query_today_closing_price')
    @patch('core.utils.market_time.date')
    def test_get_market_day_range(self, mock_date, mock_alpaca_can_query_today_closing_price):
        for test_case in get_market_day_range_test_cases:
            with self.subTest(msg=test_case["name"]):
                mock_date.today.return_value = test_case["date"]
                mock_alpaca_can_query_today_closing_price.return_value = test_case["query_today"]
                start_date, end_date = get_market_day_range(test_case["market_days_period"])
                self.assertEqual(start_date, test_case["expected_start_date"])
                self.assertEqual(end_date, test_case["expected_end_date"])
