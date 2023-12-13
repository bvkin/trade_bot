from core.utils.column import find_column_ignore_case
from core.trading.strategy import Strategy
from core.models.trade_signal import TradeSignal
import numpy as np
import pandas as pd
from talib import BBANDS, RSI

class MVWAP(Strategy):
    def __init__(self, df: pd.DataFrame) -> None:
        self.mvwap_window = 20
        self.backcandles = 10
        self.rsi_peak_prominance_factor = 1.5
        self.rsi_bullish_signal = 45
        self.rsi_bearish_signal = 55

        # Set indicators
        close = find_column_ignore_case(df, "close")
        _open = find_column_ignore_case(df, "open")
        vwap = find_column_ignore_case(df, "vwap")
        bbands_upper, _, bbands_lower = BBANDS(close, timeperiod=20, nbdevup=1.5, nbdevdn=1.5)
        # Save indicators
        self.indicators =  {
            "close": close,
            "open": _open,
            "bbands_upper": bbands_upper,
            "bbands_lower": bbands_lower,
            "rsi": RSI(close, timeperiod=14),
            "mvwap": self.get_mvwap(vwap)
        }

    def get_indicator(self, name: str) -> dict:
        """
        Returns inicator specified by input name
        """
        return self.indicators[name]

    def get_mvwap(self, vwap: pd.Series) -> pd.Series:
        """
        Calculates and returns mvwap values for a given series
        """
        return vwap.rolling(window=self.mvwap_window).mean()
    
    def get_mvwap_signal(self, open: pd.Series, close: pd.Series, mvwap: float):
        """
        If the last 15 candles are above mvwap return bullish signal
        If the last 15 candles are below mvwap return bearish signal
        Else return no clear pattern
        """
        open_close_max = np.maximum(open, close)

        # Last 15 candles above mvwap
        if (open_close_max.tail(self.backcandles) > mvwap).all():
            return TradeSignal.BULLISH
        # Last 15 candles below mvwap
        elif (open_close_max.tail(self.backcandles) < mvwap).all():
            return TradeSignal.BEARISH
        else:
            return TradeSignal.NO_CLEAR_PATTERN
    
    def signal(self, indicators: dict):
        # For compatability with backtesting
        if indicators == None:
            indicators = self.indicators
        _open = indicators["open"]
        close = indicators["close"]
        bbands_upper = indicators["bbands_upper"]
        bbands_lower = indicators["bbands_lower"]
        rsi = indicators["rsi"]
        mvwap = indicators["mvwap"]

        mvwap_signal = self.get_mvwap_signal(_open, close, float(mvwap[-1]))

        if mvwap_signal == TradeSignal.BULLISH and rsi[-1] < self.rsi_bullish_signal and close[-1] < bbands_lower[-1]:
            return TradeSignal.BULLISH
        elif mvwap_signal == TradeSignal.BULLISH and rsi[-1] > self.rsi_bearish_signal and close[-1] > bbands_upper[-1]:
            return TradeSignal.BEARISH
        else:
            return TradeSignal.NO_CLEAR_PATTERN