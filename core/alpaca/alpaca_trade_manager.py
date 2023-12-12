from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
from typing import Any, List, Optional

class AlpacaTradeManager:
    timeframes = {
        "day": TimeFrame.Day,
        "hour": TimeFrame.Hour
    }

    def __init__(self,
                 alpaca_api_key: str,
                 alpaca_secret_key: str,
                 base_url: str = "https://paper-api.alpaca.markets",
                 api_version: str = 'v2',
                 api: Optional[Any] = None) -> None:
        if api is None:
            self.api = REST(
                alpaca_api_key,
                alpaca_secret_key,
                base_url,
                api_version
            )
        else:
            self.api = api


    def get_price_data(self, ticker: str, period_start: str, period_end: str, timeframe: str = "day", adjustment: str = 'raw') -> pd.DataFrame:
        """
        Returns a pandas dataframe of the price data for last two days of a given ticker.
        """
        return self.api.get_bars(
            symbol=ticker, 
            timeframe=self.timeframes[timeframe],
            start=period_start,
            end=period_end,
            adjustment=adjustment
        ).df


    def buy_stock(self, ticker: str) -> None:
        """
        Buys 5% of the buying power of the account for a given ticker.
        Limits losses at 10% of original purchase value.
        """
        buying_power = float(self.api.get_account().buying_power)
        purchase_amnt = round(buying_power * 0.05, 2)
        floor = round(purchase_amnt * 0.9, 2)

        self.api.submit_order(
            symbol=ticker,
            notional=purchase_amnt,
            stop_loss=dict(
              stop_price=floor
            ),
            side='buy',
            type='market',
            time_in_force='day'
        )


    def sell_stock(self, ticker: str) -> None:
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


    def get_stock_qty(self, ticker: str) -> float:
        """
        Returns the quantity of a stock owned.
        """
        return [item.qty for item in  self.api.list_positions() if item.symbol == ticker][0]


    def get_owned_tickers(self) -> List[str]:
        """
        Returns a list of tickers currently held in account
        """
        return [position.symbol for position in self.api.list_positions()]
