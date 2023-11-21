from core.models.trade_signal import TradeSignal
import pandas as pd
import logging

class EngulfingCandlesticks():
    def __init__(self, open_prices, close_prices):
        try:
            self.open       = open_prices[-1]
            self.prev_open  = open_prices[-2]
            self.close      = close_prices[-1]
            self.prev_close = close_prices[-2]
        except KeyError:
            self.open       = open_prices.tolist()[-1]
            self.prev_open  = open_prices.tolist()[-2]
            self.close      = close_prices.tolist()[-1]
            self.prev_close = close_prices.tolist()[-2]
    
    def get_open(self):
        return self.open
    
    def get_prev_open(self):
        return self.prev_open
    
    def get_close(self):
        return self.close
    
    def get_prev_close(self):
        return self.get_prev_close
    
    def signal(self, open=None, prev_open=None, close=None, prev_close=None):
        # For compatability with backtesting
        if open == None:
            open = self.open
        if prev_open == None:
            prev_open = self.prev_open
        if close == None:
            close = self.close
        if prev_close == None:
            prev_close = self.prev_close


        if open > close and prev_open < prev_close and close < prev_open and open >= prev_close:
            return TradeSignal.BEARISH
        elif open < close and prev_open > prev_close and close > prev_open and open <= prev_close:
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
