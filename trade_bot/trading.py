# Ignore FutureWarning for frame.append method in yahoo_fin module until new version release
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="yahoo_fin")

from datetime import datetime, date, time, timedelta
import pytz
from yahoo_fin.stock_info import tickers_sp500
import logging
import pandas_market_calendars as mcal


# Constants for the signal generator
BEARISH, BULLISH, NO_CLEAR_PATTERN = 1, 2, 0

def get_first_last_market_days(market_days_period):
    """
    Returns a period of market days based on todays date

    Parameters:
        market_days_period (int): Number of days a market period should span, based on the current date

    Returns:
        period_start (str): An RFC-3339 string representing the start date of the period
        period_end (str): An RFC-3339 string representing the end of the period. Time is rutruned as after 4PM (eastern) if the market is done trading for the day.

    """

    # Check if it is safe to include today in time frame
    query_today = alpaca_can_query_today_closing_price()

    # Get the NYSE calendar
    nyse = mcal.get_calendar('NYSE')

    # Get today in datetime format
    today = datetime.combine(date.today(), time(0, 0))

    # Subtract 1 day if query_today=False
    offset_day = lambda x: 0 if x else 1
    end_date = today - timedelta(days=offset_day(query_today))
    start_date = end_date - timedelta(days=(market_days_period)*3)  # Assuming weekends and holidays, approx n*3 should cover it

    # Get period start and end dates
    market_days = nyse.valid_days(start_date=start_date, end_date=end_date)[-market_days_period:]
    period_start = datetime.combine(market_days[0], time(0, 0)).strftime('%Y-%m-%dT%H:%M:%S-04:00')
    period_end = datetime.combine(market_days[-1], time(16, 30)).strftime('%Y-%m-%dT%H:%M:%S-04:00')

    return period_start, period_end


def alpaca_can_query_today_closing_price():
    """
    Checks if the closing price of the day is safe to query on alpaca api 

    Returns:
        query_today (bool): True if the current time is after 4:16 PM (can query for todays closing price on alpaca free tier)
            else False
    """
    current_time = datetime.now(pytz.timezone('US/Eastern'))

    # Define the cutoff time as 16:16 (4:16 PM)
    cutoff_time = datetime.strptime("16:16", "%H:%M").time()

    query_today = current_time.time() >= cutoff_time

    return query_today


def moving_average_singnal_generator(trade_manager, ticker):
    """
    Genarates signals based on 5 and 20 day smoving averages
    Parameters:
        trade_manager (TradeManager): An instance of the TradeManager class used to manage trades.
        ticker (str): The stock ticker for which the signal is to be generated.

    Returns:
        signal (int): An in representing the signal, which could be BULLISH, BEARISH, or NO_CLEAR_PATTERN.
    """
    period_start, period_end = get_first_last_market_days(20) # If market is active, today's date is -1
    df = trade_manager.get_price_data(ticker, period_start, period_end)

    # Get 5 and 20 day moving averages
    try:
        df['day_ma_5'] = df['close'].rolling(window=5).mean()
        df['day_ma_20'] = df['close'].rolling(window=20).mean()
        day_ma_5 = df.iloc[19, df.columns.get_loc('day_ma_5')]
        day_ma_20 = df.iloc[19, df.columns.get_loc('day_ma_20')]
    except IndexError:
        logging.warning(f"Unable to get the required data for {ticker}")
        return NO_CLEAR_PATTERN
    
    # Generate signals
    if day_ma_5 > day_ma_20: # 5 day crosses above 20 day
        signal = BULLISH
    elif day_ma_5 < day_ma_20: # 5 day drops below 20 day
        signal = BEARISH
    else:
        signal = NO_CLEAR_PATTERN
    
    return signal

def engulfing_candlestick_signal_generator(trade_manager, ticker):
    """
    Returns a signal based on the price data of a given ticker.
    Uses engulfing candlestick pattern.
    """
    period_start, period_end = get_first_last_market_days(2) # If market is active, today's date is -1
    df = trade_manager.get_price_data(ticker, period_start, period_end)

    try:
        open = df.iloc[1, df.columns.get_loc('open')]
        close = df.iloc[1, df.columns.get_loc('close')]
        previous_open = df.iloc[0, df.columns.get_loc('open')]
        previous_close = df.iloc[0, df.columns.get_loc('close')]
    except IndexError:
        logging.warning(f"Unable to get the required data for {ticker}")
        return NO_CLEAR_PATTERN

    if (
        open > close and 
        previous_open < previous_close and 
        close < previous_open and
        open >= previous_close
    ):
        return BEARISH

    # Bullish Pattern
    elif (
        open < close and 
        previous_open > previous_close and 
        close > previous_open and
        open <= previous_close
    ):
        return BULLISH
    
    # No clear pattern
    else:
        return NO_CLEAR_PATTERN


def make_orders(trade_manager):
    """
    Makes buy orders for all stocks in the S&P 500 given a bullish signal.
    Makes sell orders for all owned stocks bearish signal.
    """
    logging.info("Making orders...")
    for ticker in tickers_sp500():
        ticker = ticker.replace('-', '.')
        logging.info("Evaluating " + ticker + " for buy")
        signal = moving_average_singnal_generator(trade_manager, ticker)
        if signal == BULLISH:
            trade_manager.buy_stock(ticker)
            logging.info("Buy order for " + ticker + " placed.")

    owned_tickers = trade_manager.get_owned_tickers()
    for ticker in owned_tickers:
        logging.info("Evaluating " + ticker + " for sell")
        signal = moving_average_singnal_generator(trade_manager, ticker)
        if signal == BEARISH:
            trade_manager.sell_stock(ticker)
            logging.info("Sell order for " + ticker + " placed.")
