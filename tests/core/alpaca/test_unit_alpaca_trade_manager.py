import unittest
from unittest.mock import patch, Mock
from core.alpaca.alpaca_trade_manager import AlpacaTradeManager
from alpaca_trade_api.rest import TimeFrame


class TestAlpacaTradeManager(unittest.TestCase):

    def setUp(self):
        # Create a mock API object and a TradeManager that uses it
        self.mock_api = Mock()
        self.trade_manager = AlpacaTradeManager(
            alpaca_api_key="api_key",
            alpaca_secret_key="secret_key",
            api=self.mock_api,
        )


    def test_buy_stock(self):
        """
        Tests the 'buy_stock' method of the 'AlpacaTradeManager' class.
        """
        mock_buying_power = 1000
        purchase_amnt = round(mock_buying_power * 0.05, 2)
        floor = round(purchase_amnt * 0.9, 2)

        self.mock_api.get_account = Mock(return_value=Mock(buying_power=str(mock_buying_power)))
        self.mock_api.submit_order = Mock()

        # Call the function we're testing
        self.trade_manager.buy_stock("TEST")

        # Check for expected arguments
        self.mock_api.submit_order.assert_called_with(
            symbol="TEST",
            notional=purchase_amnt,
            stop_loss=dict(
              stop_price=floor
            ),
            side='buy',
            type='market',
            time_in_force='day'
        )
        

    @patch('core.alpaca.alpaca_trade_manager.AlpacaTradeManager.get_stock_qty', return_value=10)
    def test_sell_stock(self, mock_get_stock_qty):
        """
        Tests the 'sell_stock' method of the 'AlpacaTradeManager' class.
        """
        # Call the function we're testing
        self.trade_manager.sell_stock("TEST")

        # Check for expected arguments
        self.mock_api.submit_order.assert_called_once_with(
            symbol="TEST",
            qty=10,
            side='sell',
            type='market',
            time_in_force='gtc'
        )

    def test_get_price_data(self):
        """
        Tests the 'get_price_data' method of the 'AlpacaTradeManager' class.
        """
        # Test call for day
        self.trade_manager.get_price_data("TEST", "2023-12-11", "2023-12-12", timeframe="day", adjustment="raw")
        self.mock_api.get_bars.assert_called_with(
            symbol="TEST",
            timeframe=TimeFrame.Day,
            start="2023-12-11",
            end="2023-12-12",
            adjustment="raw"
        )

        # Test call for hour
        self.trade_manager.get_price_data("TEST", "2023-12-11", "2023-12-12", timeframe="hour", adjustment="raw")
        self.mock_api.get_bars.assert_called_with(
            symbol="TEST",
            timeframe=TimeFrame.Hour,
            start="2023-12-11",
            end="2023-12-12",
            adjustment="raw"
        )

if __name__ == '__main__':
    unittest.main()
