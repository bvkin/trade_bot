from core.models.trade_signal import TradeSignal
import pandas as pd
import logging


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
