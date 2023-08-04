from datetime import datetime, date, time, timedelta
import pytz
from yahoo_fin.stock_info import tickers_sp500
import logging
import pandas_market_calendars as mcal


# Constants for the signal generator
BEARISH, BULLISH, NO_CLEAR_PATTERN = 1, 2, 0

def get_first_last_market_days(market_days_period, query_today=False):
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
    period_start = market_days[0].strftime('%Y-%m-%d')
    period_end = market_days[-1].strftime('%Y-%m-%d')

    # Add market close time if today is included in query
    if query_today and today.strftime('%Y-%m-%d') == period_end:
        period_end_datetime = datetime.strptime(period_end, '%Y-%m-%d')
        period_end = datetime.combine(period_end_datetime, time(16, 30)).strftime('%Y-%m-%dT%H:%M:%S-04:00')

    return period_start, period_end


def is_after_alpaca_market_hours():
    """
    Returns true if the current time is after 4:16 PM (when it is safe to query for stock closing prices)
    else returns false
    """
    current_time = datetime.now(pytz.timezone('US/Eastern'))

    # Define the cutoff time as 16:16 (4:16 PM)
    cutoff_time = datetime.strptime("16:16", "%H:%M").time()

    return current_time.time() >= cutoff_time


def engulfing_candlestick_signal_generator(trade_manager, symbol):
    """
    Returns a signal based on the price data of a given ticker.
    Uses engulfing candlestick pattern.
    """
    period_start, period_end = get_first_last_market_days(2, query_today=is_after_alpaca_market_hours()) # If market is active, today's date is -1
    df = trade_manager.get_price_data(symbol, period_start, period_end)

    try:
        open = df.iloc[1, df.columns.get_loc('open')]
        close = df.iloc[1, df.columns.get_loc('close')]
        previous_open = df.iloc[0, df.columns.get_loc('open')]
        previous_close = df.iloc[0, df.columns.get_loc('close')]
    except IndexError:
        logging.warning(f"Unable to get the required data for {symbol}")
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
    for ticker in tickers_sp500()[0:10]:
        ticker = ticker.replace('-', '.')
        signal = engulfing_candlestick_signal_generator(trade_manager, ticker)
        if signal == BULLISH:
            trade_manager.buy_stock(ticker)
            logging.info("Buy order for " + ticker + " placed.")

    owned_tickers = trade_manager.get_owned_tickers()
    for ticker in owned_tickers:
        signal = engulfing_candlestick_signal_generator(trade_manager, ticker)
        if signal == BEARISH:
            trade_manager.sell_stock(ticker)
            logging.info("Sell order for " + ticker + " placed.")
