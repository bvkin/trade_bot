from core.models.trade_signal import TradeSignal
from core.trading.strategy import Strategy
from core.utils.column import find_column_ignore_case
from talib import CDLENGULFING

class EngulfingCandlesticks(Strategy):
    def __init__(self, df):
        self.signals = CDLENGULFING(
            open=find_column_ignore_case(df, "open"),
            high=find_column_ignore_case(df, "high"),
            low=find_column_ignore_case(df, "low"),
            close=find_column_ignore_case(df, "close")
        )
    
    def get_signals(self):
        return self.signals

    def signal(self, signals=None):
        # For compatability with backtesting
        if signals == None:
            signals = self.signals.tolist()

        if signals[-1] == -100:
            return TradeSignal.BEARISH
        elif signals[-1] == 100:
            return TradeSignal.BULLISH
        else:
            return TradeSignal.NO_CLEAR_PATTERN
            