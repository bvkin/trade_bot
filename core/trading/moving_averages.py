from core.models.trade_signal import TradeSignal
from core.trading.strategy import Strategy
from core.utils.column import find_column_ignore_case
import logging
import pandas as pd
from talib import SMA

class MovingAverages(Strategy):
    def __init__(self, df, short_window=5, long_window=20):
        self.close_prices = find_column_ignore_case(df, 'close')
        self.short_window_ma = self.gen_ma(short_window)
        self.long_window_ma = self.gen_ma(long_window)

    def get_short_window_ma(self):
        return self.short_window_ma

    def get_long_window_ma(self):
        return self.long_window_ma

    def gen_ma(self, window: int) -> pd.Series:
        try:
            return SMA(self.close_prices, timeperiod=window)
        except IndexError:
            logging.warning(f"Unable to interpret required data")
            return []
    
    def signal(self, short_window_ma=None, long_window_ma=None) -> TradeSignal:
        # For compatability with backtesting
        if short_window_ma == None:
            short_window_ma = self.short_window_ma.tolist()
        if long_window_ma == None:
            long_window_ma = self.long_window_ma.tolist()

        # Generate signals
        if short_window_ma[-1] > long_window_ma[-1] and short_window_ma[-2] <= long_window_ma[-2]: # 5 day crosses above 20 day
            return TradeSignal.BULLISH
        elif short_window_ma[-1] < long_window_ma[-1] and short_window_ma[-2] >= long_window_ma[-2]: # 5 day drops below 20 day
            return TradeSignal.BEARISH
        else:
            return TradeSignal.NO_CLEAR_PATTERN
