import unittest
from unittest.mock import patch, Mock
from trade_bot.alpaca_trade_manager import AlpacaTradeManager
from yahoo_fin import stock_info as si

class TestAlpacaTradeManager(unittest.TestCase):

    def setUp(self):
        # Create a mock API object and a TradeManager that uses it
        self.mock_api = Mock()
        self.trade_manager = AlpacaTradeManager(
            alpaca_api_key="api_key",
            alpaca_secret_key="secret_key",
            api=self.mock_api,
        )


    @patch.object(si, 'get_quote_table', return_value={'Quote Price': 10})
    def test_buy_stock(self, mock_get_quote_table):
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
<<<<<<< HEAD
            time_in_force='day'
=======
            time_in_force='gtc'
>>>>>>> aba9b37 (Notional Orders (#4))
        )
        

    @patch('trade_bot.alpaca_trade_manager.AlpacaTradeManager.get_stock_qty', return_value=10)
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


if __name__ == '__main__':
    unittest.main()
