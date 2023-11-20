from core.alpaca.alpaca_trade_manager import AlpacaTradeManager
from core.models.trade_signal import TradeSignal
from core.utils.market_time import get_market_day_range
from boto3_type_annotations.sns import Client as SNSClient
import pandas as pd
import talib
from typing import List
import logging


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


def make_orders(trade_manager: AlpacaTradeManager, tickers: List[str], sns_client: SNSClient,  sns_topic_arn: str = None) -> None:
    """
    Makes buy orders for all stocks in the S&P 500 given a bullish signal.
    Makes sell orders for all owned stocks bearish signal.
    """
    purchased_tickers, sold_tickers = [], []
    period_start, period_end = get_market_day_range(21) # 21 for 20 day moving avg

    logging.info("Making orders...")
    for ticker in tickers:
        logging.info("Evaluating " + ticker + " for buy")
        df = trade_manager.get_price_data(ticker, period_start, period_end)
        signal = moving_average_signal_generator(df.close)
        if signal == TradeSignal.BULLISH:
            trade_manager.buy_stock(ticker)
            logging.info("Buy order for " + ticker + " placed.")
            purchased_tickers.append(ticker)

    if purchased_tickers and sns_topic_arn != None:
        sns_client.publish(Message=f'Trade Bot Buy Orders Made: {", ".join(purchased_tickers)}', TopicArn=sns_topic_arn)

    owned_tickers = trade_manager.get_owned_tickers()

    for ticker in owned_tickers:
        logging.info("Evaluating " + ticker + " for sell")
        df = trade_manager.get_price_data(ticker, period_start, period_end)
        signal = moving_average_signal_generator(df.close)
        if signal == TradeSignal.BEARISH:
            trade_manager.sell_stock(ticker)
            logging.info("Sell order for " + ticker + " placed.")
            sold_tickers.append(ticker)

    if sold_tickers and sns_topic_arn != None:
        sns_client.publish(Message=f'Trade Bot Sell Orders Made: {", ".join(sold_tickers)}', TopicArn=sns_topic_arn)
