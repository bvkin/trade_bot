import datetime
import unittest
from unittest.mock import patch, Mock
from trade_bot.alpaca_trade_manager import AlpacaTradeManager
from yahoo_fin import stock_info as si

class TestAlpacaTradeManager(unittest.TestCase):

    def setUp(self):
        # Create a mock API object and a TradeManager that uses it
        self.mock_api = Mock()
        self.trade_manager = AlpacaTradeManager(alpaca_api_key="api_key", alpaca_secret_key="secret_key", api=self.mock_api,)


    @patch.object(si, 'get_quote_table', return_value={'Quote Price': 10})
    def test_buy_stock(self, mock_get_quote_table):
        # Mock the get_account method of the API to return a test value
        self.mock_api.get_account = Mock(return_value=Mock(buying_power="1000.00"))
        # Mock the submit_order method of the API to do nothing
        self.mock_api.submit_order = Mock()

        # Call the function we're testing
        self.trade_manager.buy_stock("TEST")

        # Check that submit_order was called with the expected arguments
        self.mock_api.submit_order.assert_called_with(
            symbol="TEST", qty=5, side='buy', type='market', time_in_force='gtc')
        

    @patch('trade_bot.alpaca_trade_manager.AlpacaTradeManager.get_stock_qty', return_value=10)
    def test_sell_stock(self, mock_get_stock_qty):
        self.trade_manager.sell_stock("TEST")

        # Check the result
        self.mock_api.submit_order.assert_called_once_with(
            symbol="TEST",
            qty=10,
            side='sell',
            type='market',
            time_in_force='gtc'
        )


    def test__get_trade_period(self):
        atm = AlpacaTradeManager(alpaca_api_key="api_key", alpaca_secret_key="secret_key")

        # If today is Monday (weekday = 0)
        today = datetime.date(2023, 8, 7)
        self.assertEqual(atm._get_trade_period(today), (datetime.date(2023, 8, 3), datetime.date(2023, 8, 4)))

        # If today is Tuesday (weekday = 1)
        today = datetime.date(2023, 8, 8)
        self.assertEqual(atm._get_trade_period(today), (datetime.date(2023, 8, 4), datetime.date(2023, 8, 7)))

        # If today is some other day (e.g., Wednesday)
        today = datetime.date(2023, 8, 9)
        self.assertEqual(atm._get_trade_period(today), (datetime.date(2023, 8, 7), datetime.date(2023, 8, 8)))

if __name__ == '__main__':
    unittest.main()
