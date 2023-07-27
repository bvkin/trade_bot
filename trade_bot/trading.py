from alpaca_trade_manager import AlpacaTradeManager
from yahoo_fin.stock_info import tickers_sp500
import logging

trade_manager = AlpacaTradeManager()

# Constants for the signal generator
BEARISH, BULLISH, NO_CLEAR_PATTERN = 1, 2, 0


def signal_generator(symbol):
    """
    Returns a signal based on the price data of a given ticker.
    Uses engulfing candlestick pattern.
    """
    df = trade_manager.get_price_data(symbol)

    try:
        open = df.iloc[1, df.columns.get_loc('open')]
        close = df.iloc[1, df.columns.get_loc('close')]
        previous_open = df.iloc[1, df.columns.get_loc('open')]
        previous_close = df.iloc[1, df.columns.get_loc('open')]
    except IndexError:
        logging.warning(f"Unable to get the required data for {symbol}")
        return NO_CLEAR_PATTERN

    # Bearish Pattern
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


def make_orders():
    """
    Makes buy orders for all stocks in the S&P 500 given a bullish signal.
    Makes sell orders for all owned stocks bearish signal.
    """
    logging.info("Making orders...")
    for ticker in tickers_sp500()[0:10]:
        ticker = ticker.replace('-', '.')
        signal = signal_generator(ticker)
        if signal == BULLISH:
            trade_manager.buy_stock(ticker)
            logging.info("Buy order for " + ticker + " placed.")

    owned_tickers = [position.symbol for position in trade_manager.api.list_positions()]
    for ticker in owned_tickers:
        signal = signal_generator(ticker)
        logging.info(ticker + ": " + str(signal))
        if signal == BEARISH:
            trade_manager.sell_stock(ticker)
            logging.info("Sell order for " + ticker + " placed.")
