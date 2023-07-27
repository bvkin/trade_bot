from alpaca_trade_api.rest import REST, TimeFrame
import datetime
from yahoo_fin.stock_info import get_quote_table

import os

class AlpacaTradeManager:
    def __init__(self, alpaca_api_key: str, alpaca_secret_key: str, base_url: str = "https://paper-api.alpaca.markets", api_version: str = 'v2'):
        self.api = REST(
            alpaca_api_key, 
            alpaca_secret_key,
            "https://paper-api.alpaca.markets",
            api_version='v2'
        )


    @staticmethod
    def _get_trade_period(today):
        weekday = today.weekday()

        # If today is Monday
        if weekday == 0:
            period_end = today - datetime.timedelta(days=3)
            period_start = today - datetime.timedelta(days=4)
        # If today is Tuesday
        elif weekday == 1:
            period_end = today - datetime.timedelta(days=1)
            period_start = today - datetime.timedelta(days=4)
        else:
            period_end = today - datetime.timedelta(days=1)
            period_start = today - datetime.timedelta(days=2)

        return period_start, period_end


    def get_price_data(self, ticker):
        """
        Returns a pandas dataframe of the price data for last two days of a given ticker.
        """
        today = datetime.date.today()
        period_start, period_end = self._get_trade_period(today)

        return self.api.get_bars(ticker, TimeFrame.Day, period_start, period_end, adjustment='raw').df


    def buy_stock(self, ticker):
        """
        Buys 5% of the buying power of the account for a given .
        """
        buying_power = float(self.api.get_account().buying_power)
        purchase_amnt = round(buying_power * 0.05, 2)
        share_price = get_quote_table(ticker)['Quote Price']
        shares = int(purchase_amnt / share_price)
        self.api.submit_order(
            symbol=ticker,
            qty=shares,
            side='buy',
            type='market',
            time_in_force='gtc'
        )


    def sell_stock(self, ticker):
        """
        Sells all shares of a stock.
        """
        self.api.submit_order(
            symbol=ticker,
            qty=self.get_stock_qty(ticker),
            side='sell',
            type='market',
            time_in_force='gtc'
        )


    def get_stock_qty(self, ticker):
        """
        Returns the quantity of a stock owned.
        """
        positions = self.api.list_positions()
        return [item.qty for item in positions if item.symbol == ticker][0]
