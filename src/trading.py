from alpaca_trade_manager import AlpacaTradeManager
from yahoo_fin.stock_info import tickers_sp500


trade_manager = AlpacaTradeManager()

def signal_generator(symbol):
    """
    Returns a signal based on the price data of a given ticker.
    Uses engulfing candlestick pattern.
    """
    df = trade_manager.get_price_data(symbol)

    open = df.iloc[1, df.columns.get_loc('open')]
    close = df.iloc[1, df.columns.get_loc('close')]
    previous_open = df.iloc[1, df.columns.get_loc('open')]
    previous_close = df.iloc[1, df.columns.get_loc('open')]
    
    # Bearish Pattern
    if (
        open>close and 
        previous_open<previous_close and 
        close<previous_open and
        open>=previous_close
    ):
        return 1

    # Bullish Pattern
    elif (
        open<close and 
        previous_open>previous_close and 
        close>previous_open and
        open<=previous_close
    ):
        return 2
    
    # No clear pattern
    else:
        return 0


def make_orders():
    """
    Makes buy orders for all stocks in the S&P 500 given a bullish signal.
    Makes sell orders for all owned stocks bearish signal.
    """
    print("Making orders...")
    for ticker in tickers_sp500()[0:10]:
        ticker = ticker.replace('-', '.')
        signal = signal_generator(ticker)
        print(ticker + ": " + str(signal))
        if signal == 2:
            trade_manager.buy_stock(ticker)
            print("Buy order for " + ticker + " placed.")

    owned_tickers = [position.symbol for position in trade_manager.api.list_positions()]
    for ticker in owned_tickers:
        signal = signal_generator(ticker)
        print(ticker + ": " + str(signal))
        if signal == 1:
            trade_manager.sell_stock(ticker)
            print("Sell order for " + ticker + " placed.")
