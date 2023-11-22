from core.models.trade_signal import TradeSignal
import pandas as pd
import logging
import numpy as np
from talib import CDLENGULFING

class EngulfingCandlesticks():
    def __init__(self, open_prices, high_prices, low_prices, close_prices):
        self.signals = CDLENGULFING(
            open=open_prices,
            high=high_prices,
            low=low_prices,
            close=close_prices
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
            