import datetime
from yahoo_fin.stock_info import tickers_sp500
import logging
import pandas_market_calendars as mcal


# Constants for the signal generator
BEARISH, BULLISH, NO_CLEAR_PATTERN = 1, 2, 0

def get_first_last_market_days(n):
    # Get the NYSE calendar
    nyse = mcal.get_calendar('NYSE')

    end_date = datetime.datetime.now() - datetime.timedelta(days=1)
    start_date = end_date - datetime.timedelta(days=(n)*4)  # Assuming weekends and holidays, approx n*2 should cover it

    market_days = nyse.valid_days(start_date=start_date, end_date=end_date)

    market_days = market_days[-n:]

    period_start = market_days[0].strftime('%Y-%m-%d')
    period_end = market_days[-1].strftime('%Y-%m-%d')

    return period_start, period_end


def engulfing_candlestick_signal_generator(trade_manager, symbol):
    """
    Returns a signal based on the price data of a given ticker.
    Uses engulfing candlestick pattern.
    """
    period_start, period_end = get_first_last_market_days(2)
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
