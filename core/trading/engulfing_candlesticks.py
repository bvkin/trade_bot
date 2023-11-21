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
            

def engulfing_candlestick_signal_generator(df: pd.DataFrame) -> TradeSignal:
    """
    Returns a signal based on the price data of a given ticker.
    Uses engulfing candlestick pattern.
    Parameters:
        df (TradeManager): A pandas dataframe of format from Alpaca Trade API for which to check moving averages

    Returns:
        signal (TradeSignal): An enum object representing if the strategy signals buy/sell/hold
    """
    try:
        open = df.iloc[1, df.columns.get_loc('open')]
        close = df.iloc[1, df.columns.get_loc('close')]
        previous_open = df.iloc[0, df.columns.get_loc('open')]
        previous_close = df.iloc[0, df.columns.get_loc('close')]
    except IndexError:
        logging.warning(f"Unable to interpret required data")
        return TradeSignal.NO_CLEAR_PATTERN

    if (
        open > close and 
        previous_open < previous_close and 
        close < previous_open and
        open >= previous_close
    ):
        return TradeSignal.BEARISH

    # Bullish Pattern
    elif (
        open < close and 
        previous_open > previous_close and 
        close > previous_open and
        open <= previous_close
    ):
        return TradeSignal.BULLISH
    
    # No clear pattern
    else:
        return TradeSignal.NO_CLEAR_PATTERN
