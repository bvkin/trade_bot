from core.utils.column import find_column_ignore_case
from core.trading.strategy import Strategy
from core.models.trade_signal import TradeSignal
from scipy.signal import find_peaks
from numpy import percentile
from talib import BBANDS, RSI
import pandas as pd


class EngulfingCandlesticks(Strategy):
    def __init__(self, df: pd.DataFrame) -> None:
        self.close=find_column_ignore_case(df, "close")
        self.bbands_upper, self.bbands_middle, self.bbands_lower = BBANDS(self.close, timeperiod=20)
        self.rsi = RSI(self.close, timeperiod=14)

    def get_indicators(self):
        return {
            "bbands_upper": self.bbands_upper,
            "bbands_middle": self.bbands_middle,
            "bbands_lower": self.bbands_lower,
            "rsi": self.rsi
        }
    
    def rsi_lows(self):
        inverse = -self.rsi
        prominence_threshold = inverse.std() * 1.5
        low_indicies, _ = find_peaks(inverse.values, prominence=prominence_threshold)
        rsi_lows  = self.rsi.iloc[low_indicies]
        return rsi_lows
    
    def close_lows(self):
        tail = self.close.tail(60)
        inverse = -tail
        prominence_threshold = inverse.std()
        low_indicies, _ = find_peaks(inverse.values, prominence=prominence_threshold)
        close_lows = self.close.iloc[low_indicies]
        return close_lows
    
    def trading_sideways(self):
        band_width = self.bbands_upper - self.bbands_lower
        current_band_width = band_width[-1]
        side_ways_percentile = percentile(band_width.dropna(), 20)
        is_sideways = current_band_width <= side_ways_percentile
        return is_sideways

    def signal(self):
        if self.trading_sideways():
            close_lows = self.close_lows()
            rsi_lows = self.rsi_lows()
            if close_lows[-1] < close_lows[-2] and rsi_lows[-1] > rsi_lows[-2]:
                return TradeSignal.BULLISH
            else:
                return TradeSignal.BEARISH
        else:
            if float(self.close[-1]) < float(self.bbands_lower[-1]) and self.rsi[-1] < 25:
                return TradeSignal.BULLISH
            elif float(self.close[-1]) > float(self.bbands_upper[-1]) and self.rsi[-1] > 75:
                return TradeSignal.BEARISH
