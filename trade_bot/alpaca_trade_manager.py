from alpaca_trade_api.rest import REST, TimeFrame
from yahoo_fin import stock_info as si

class AlpacaTradeManager:
    def __init__(self, alpaca_api_key: str, alpaca_secret_key: str, base_url: str = "https://paper-api.alpaca.markets", api_version: str = 'v2', api=None):
        if api is None:
            self.api = REST(
                alpaca_api_key,
                alpaca_secret_key,
                base_url,
                api_version
            )
        else:
            self.api = api


    def get_price_data(self, ticker, period_start, period_end):
        """
        Returns a pandas dataframe of the price data for last two days of a given ticker.
        """
        # return self.api.get_bars(ticker, TimeFrame.Day, period_start, period_end, adjustment='raw').df
        return self.api.get_bars(ticker, TimeFrame.Day, period_start, period_end, adjustment='raw').df


    def buy_stock(self, ticker):
        """
        Buys 5% of the buying power of the account for a given ticker.
        Limits losses at 10% of original purchase value.

        CHANGES...
        -> Notional Order Type, Sell Limit
        -> Reason for Change(s)
        -> Result in Effect
        -> Further Considerations
        """
        buying_power = float(self.api.get_account().buying_power)
        #purchase_amnt = round(buying_power * 0.05, 2)
        value = round(buying_power * 0.05, 2)
        # share_price = si.get_quote_table(ticker)['Quote Price']
        # shares = int(purchase_amnt / share_price)
        floor = round(value * 0.9, 2)

        self.api.submit_order(
            symbol=ticker,
            notional=value,
            stop_loss=dict(
              stop_price=floor,
              limit_price=floor,
            ),
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
        return [item.qty for item in  self.api.list_positions() if item.symbol == ticker][0]


    def get_owned_tickers(self):
        """
        Returns a list of tickers currently held in account
        """
        return [position.symbol for position in self.api.list_positions()]
