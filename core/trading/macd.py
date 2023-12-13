from core.models.trade_signal import TradeSignal
from core.trading.strategy import Strategy
from core.utils.column import find_column_ignore_case
import logging
import pandas as pd
from talib import SMA, MACDEXT

class MACD(Strategy):
    """
    Class representing the moving averages trading strategy
    Short and long windows are customizable on init
    """
    def __init__(self, df: pd.DataFrame):
        close = find_column_ignore_case(df, "close")
        macd, macdsignal, macdhist = MACDEXT(close, fastperiod=12, slowperiod=26, signalperiod=9)

        self.indicators = {
            "close": close,
            "macd": macd,
            "macdsignal": macdsignal,
            "macdhist": macdhist,
            "window_ma_200":  self.gen_ma(close, 200).tolist()
        }

    def get_indicator(self, name: str) -> dict:
        """
        Returns inicator specified by input name
        """
        return self.indicators[name]

    def gen_ma(self, closes: pd.Series, window: int) -> pd.Series:
        """
        Uses talib to generate a moving average based on an input window size
        """
        try:
            return SMA(closes, timeperiod=window)
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
        macd = indicators["macd"]
        macdsignal = indicators["macdsignal"]
        window_ma_200 = indicators["window_ma_200"]

        if macd[-1] > macdsignal[-1] and macd[-2] <= macdsignal[-2] and close[-1] > window_ma_200[-1]:
            return TradeSignal.BULLISH
        elif  macd[-1] < macdsignal[-1] and macd[-2] >= macdsignal[-2] and close[-1] < window_ma_200[-1]:
            return TradeSignal.BEARISH
        else:
            return TradeSignal.NO_CLEAR_PATTERN

