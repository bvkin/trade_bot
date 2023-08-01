from datetime import datetime, timedelta
from yahoo_fin.stock_info import tickers_sp500
import logging
import pandas_market_calendars as mcal


# Constants for the signal generator
BEARISH, BULLISH, NO_CLEAR_PATTERN = 1, 2, 0

def get_first_last_market_days(market_days_period, market_active=False):
    # Get the NYSE calendar
    nyse = mcal.get_calendar('NYSE')

    if market_active:
        market_offset = 1
    else:
        market_offset = 0

    end_date = datetime.now() - timedelta(days=market_offset)
    start_date = end_date - timedelta(days=(market_days_period)*4)  # Assuming weekends and holidays, approx n*2 should cover it

    market_days = nyse.valid_days(start_date=start_date, end_date=end_date)

    market_days = market_days[-market_days_period:]

    period_start = market_days[0].strftime('%Y-%m-%d')
    period_end = market_days[-1].strftime('%Y-%m-%d')

    return period_start, period_end

def is_market_active():
    """
    Check if the market is currently active
    We give a 15 minute buffer for the market close because Alpaca api will not allow the return of
    market data from the past 15 minutes of a free plan
    """
    # Check if today is a weekday (0=Monday, 6=Sunday)
    if datetime.today().weekday() >= 5:
        return False

    # Get Current time
    current_time = datetime.now().time()

    # Set market open and close times (+15 min for close)
    market_open_time = datetime.strptime("09:30", "%H:%M").time()
    market_close_time = datetime.strptime("16:15", "%H:%M").time()

    # Check if the current time is within the market hours
    if market_open_time <= current_time <= market_close_time:
        return True
    else:
        return False


def engulfing_candlestick_signal_generator(trade_manager, symbol):
    """
    Returns a signal based on the price data of a given ticker.
    Uses engulfing candlestick pattern.
    """
    period_start, period_end = get_first_last_market_days(2, market_active=is_market_active()) # If market is active, today's date is -1
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

    owned_tickers = [position.symbol for position in trade_manager.api.list_positions()]
    for ticker in owned_tickers:
        signal = engulfing_candlestick_signal_generator(trade_manager, ticker)
        if signal == BEARISH:
            trade_manager.sell_stock(ticker)
            logging.info("Sell order for " + ticker + " placed.")
