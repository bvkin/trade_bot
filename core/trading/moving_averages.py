from core.models.trade_signal import TradeSignal
import logging
import pandas as pd
import talib

class MovingAverages():
    def __init__(self, close_prices):
        self.close_prices = close_prices

    def gen_moving_average(self, window: int) -> pd.Series:
        try:
            return talib.SMA(self.close_prices, timeperiod=window)
        except IndexError:
            logging.warning(f"Unable to interpret required data")
            return []
        
    def signal(self, short_window_ma, long_window_ma) -> TradeSignal:
        # Generate signals
        if short_window_ma[-1] > long_window_ma[-1] and short_window_ma[-2] <= long_window_ma[-2]: # 5 day crosses above 20 day
            return TradeSignal.BULLISH
        elif short_window_ma[-1] < long_window_ma[-1] and short_window_ma[-2] >= long_window_ma[-2]: # 5 day drops below 20 day
            return TradeSignal.BEARISH
        else:
            return TradeSignal.NO_CLEAR_PATTERN
        
def moving_average_signal_generator(closes: pd.Series, short_window: int = 5, long_window: int = 20) -> TradeSignal:
    """
    Genarates signals based on 5 and 20 day smoving averages
    Parameters:
        closes (pd.Series): A pandas series representing close prices for a stock
        short_window (int): Integer value representing shorter moving average window
        long_window (int): Integer value representing longer moving average window
    Returns:
        signal (TradeSignal): An enum object representing if the strategy signals buy/sell/hold
    """
    # Get moving averages for short and long windows
    # Grab tail of long_window +1 for to prevent longer roller periods when backtesting
    try:
        short_window_ma = talib.SMA(closes.tail(long_window + 1), timeperiod=short_window).values
        long_window_ma = talib.SMA(closes.tail(long_window + 1), timeperiod=long_window).values
    except IndexError:
        logging.warning(f"Unable to interpret required data")
        return TradeSignal.NO_CLEAR_PATTERN
    
    # Generate signals
    if short_window_ma[-1] > long_window_ma[-1] and short_window_ma[-2] <= long_window_ma[-2]: # 5 day crosses above 20 day
        return TradeSignal.BULLISH
    elif short_window_ma[-1] < long_window_ma[-1] and  short_window_ma[-2] >= long_window_ma[-2]: # 5 day drops below 20 day
        return TradeSignal.BEARISH
    else:
        return TradeSignal.NO_CLEAR_PATTERN
