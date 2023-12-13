from core.models.trade_signal import TradeSignal
from core.trading.strategy import Strategy
from core.utils.column import find_column_ignore_case
import logging
import pandas as pd
from talib import SMA

class MovingAverages(Strategy):
    """
    Class representing the moving averages trading strategy
    Short and long windows are customizable on init
    """
    def __init__(self, df: pd.DataFrame, short_window: int = 5, long_window: int = 20):
        close = find_column_ignore_case(df, 'close')
        self.indicators = {
            "close": close.tolist(),
            "short_window_ma": self.gen_ma(close, short_window).tolist(),
            "long_window_ma": self.gen_ma(close, long_window).tolist(),
            "window_ma_200": self.gen_ma(close, 200).tolist(),
        }

    def get_indicator(self, name: str) -> dict:
        """
        Returns inicator specified by input name
        """
        return self.indicators[name]

    def gen_ma(self, close: pd.Series, window: int) -> pd.Series:
        """
        Uses talib to generate a moving average based on an input window size
        """
        try:
            return SMA(close, timeperiod=window)
        except IndexError:
            logging.warning(f"Unable to interpret required data")
            return []
    
    def signal(self, indicators: dict = None) -> TradeSignal:
        """
        Returns a trade signal for the most recent day based on moving average cross overs
        """
        # For compatability with backtesting
        if indicators == None:
            indicators = self.indicators

        close = indicators["close"]
        short_window_ma = indicators["short_window_ma"]
        long_window_ma = indicators["long_window_ma"]
        window_ma_200 = indicators["window_ma_200"]

        # Generate signals
        if short_window_ma[-1] > long_window_ma[-1] and short_window_ma[-2] <= long_window_ma[-2] and close[-1] > window_ma_200[-1]: # 5 day crosses above 20 day
            return TradeSignal.BULLISH
        elif short_window_ma[-1] < long_window_ma[-1] and short_window_ma[-2] >= long_window_ma[-2] and close[-1] < window_ma_200[-1]: # 5 day drops below 20 day
            return TradeSignal.BEARISH
        else:
            return TradeSignal.NO_CLEAR_PATTERN
