from core.models.trade_signal import TradeSignal
from core.trading.strategy import Strategy
from core.utils.column import find_column_ignore_case
import pandas as pd
from talib import CDLENGULFING

class EngulfingCandlesticks(Strategy):
    """
    Class representing the engulfing candlesticks trading strategy
    """
    def __init__(self, df: pd.DataFrame) -> None:
        self.indicators = {
            "signals" : CDLENGULFING(
                            open=find_column_ignore_case(df, "open"),
                            high=find_column_ignore_case(df, "high"),
                            low=find_column_ignore_case(df, "low"),
                            close=find_column_ignore_case(df, "close")
            ).tolist()
        }
        
    
    def get_indicator(self, name) -> pd.Series:
        """
        Returns inicator specified by input name
        """
        return self.indicators[name]

    def signal(self, indicators: dict = None) -> TradeSignal:
        """
        Returns a trade signal for the most recent day in the self.signals series
        """
        # For compatability with backtesting
        if indicators == None:
            indicators = self.indicators

        signals = indicators["signals"]

        if signals[-1] == -100:
            return TradeSignal.BEARISH
        elif signals[-1] == 100:
            return TradeSignal.BULLISH
        else:
            return TradeSignal.NO_CLEAR_PATTERN
            