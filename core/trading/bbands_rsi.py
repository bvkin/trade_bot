from core.utils.column import find_column_ignore_case
from core.trading.strategy import Strategy
from core.models.trade_signal import TradeSignal
from scipy.signal import find_peaks
from talib import BBANDS, RSI
import pandas as pd


class BBandsRSI(Strategy):
    def __init__(self, df: pd.DataFrame) -> None:
        self.trading_sideways_threshold = 0.20
        self.rsi_peak_prominance_factor = 1.5
        self.close_peak_prominance_factor = 1

        # Set indicators
        close = find_column_ignore_case(df, "close")
        bbands_upper, bbands_middle, bbands_lower = BBANDS(close, timeperiod=20)
        # Save indicators
        self.indicators =  {
            "close": close,
            "bbands_upper": bbands_upper,
            "bbands_middle": bbands_middle,
            "bbands_lower": bbands_lower,
            "trading_sideways": self.trading_sideways(bbands_upper, bbands_lower),
            "rsi": RSI(close, timeperiod=14)
        }
    
    def get_indicator(self, name: str) -> dict:
        """
        Returns inicator specified by input name
        """
        return self.indicators[name]

    def rsi_divergence(self, rsi):
        inverse = -rsi
        prominence_threshold = inverse.std() * self.rsi_peak_prominance_factor
        low_indicies, _ = find_peaks(inverse.values, prominence=prominence_threshold)
        if len(low_indicies) < 2:
            return False
        rsi_lows  = rsi.iloc[low_indicies]
        return rsi_lows[-1] > rsi_lows[-2]
    
    def close_divergence(self, close):
        inverse = -close
        prominence_threshold = inverse.std() * self.close_peak_prominance_factor
        low_indicies, _ = find_peaks(inverse.values, prominence=prominence_threshold)
        if len(low_indicies) < 2:
            return False
        close_lows  = close.iloc[low_indicies]
        return close_lows[-1] < close_lows[-2]
    
    def trading_sideways(self, bbands_upper, bbands_lower):
        band_width = bbands_upper - bbands_lower
        quantile = band_width.quantile(self.trading_sideways_threshold)
        is_sideways = band_width < quantile
        return is_sideways

    def signal(self, indicators: dict = None):
        # For compatability with backtesting
        if indicators == None:
            indicators = self.indicators

        close = indicators["close"]
        bbands_upper = indicators["bbands_upper"]
        bbands_lower = indicators["bbands_lower"]
        trading_sideways = indicators["trading_sideways"]
        rsi = indicators["rsi"]

        if trading_sideways.iloc[-1]:
            if self.close_divergence(close) and self.rsi_divergence(rsi):
                print("bullish on trade sideways!")
                return TradeSignal.BULLISH
            else:
                return TradeSignal.BEARISH

        if float(close[-1]) < float(bbands_lower[-1]) and float(rsi[-1]) < 30:
            return TradeSignal.BULLISH
        elif float(close[-1]) > float(bbands_upper[-1]) and float(rsi[-1]) > 70:
            return TradeSignal.BEARISH
        else:
            return TradeSignal.NO_CLEAR_PATTERN
