from alpaca_trade_api.rest import REST, TimeFrame
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from yahoo_fin.stock_info import tickers_sp500, get_quote_table


import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('ALPACA_API_KEY')
SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')

api = REST(
    API_KEY, 
    SECRET_KEY,
    "https://paper-api.alpaca.markets",
    api_version='v2'
)


def signal_generator(symbol):
    """
    Returns a signal based on the price data of a given ticker.
    Uses engulfing candlestick pattern.
    """
    df = get_price_data(symbol)

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

def get_price_data(ticker):
    """
    Returns a pandas dataframe of the price data for last two days of a given ticker.
    """
    period_end = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    period_start = (datetime.date.today() - datetime.timedelta(days=4)).strftime("%Y-%m-%d")

    return api.get_bars(ticker, TimeFrame.Day, period_start, period_end, adjustment='raw').df


def buy_stock(ticker):
    """
    Buys 5% of the buying power of the account for a given .
    """
    buying_power = float(api.get_account().buying_power)
    purchase_amnt = round(buying_power * 0.05, 2)
    share_price = get_quote_table(ticker)['Quote Price']
    shares = int(purchase_amnt / share_price)
    api.submit_order(
        symbol=ticker,
        qty=shares,
        side='buy',
        type='market',
        time_in_force='gtc'
    )

def sell_stock(ticker):
    """
    Sells all shares of a stock.
    """
    api.submit_order(
        symbol=ticker,
        qty=get_stock_qty(ticker),
        side='sell',
        type='market',
        time_in_force='gtc'
    )

def get_stock_qty(ticker):
    """
    Returns the quantity of a stock owned.
    """
    positions = api.list_positions()
    return [item.qty for item in positions if item.symbol == ticker][0]

def make_orders():
    """
    Makes buy orders for all stocks in the S&P 500 given a bullish signal.
    Makes sell orders for all owned stocks bearish signal.
    """
    print("Making orders...")
    for ticker in tickers_sp500()[0:10]:
        ticker = ticker.replace('-', '.')
        signal = signal_generator(ticker)
        if signal == 2:
            buy_stock(ticker)
            print("Buy order for " + ticker + " placed.")

    owned_tickers = [position.symbol for position in api.list_positions()]
    for ticker in owned_tickers:
        signal = signal_generator(ticker)
        if signal == 1:
            sell_stock(ticker)
            print("Sell order for " + ticker + " placed.")


if __name__ == '__main__':
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scheduler = BlockingScheduler()
    scheduler.add_job(make_orders, 'cron', start_date=current_time, day_of_week='mon-fri',hour=9, timezone='US/Eastern')
    scheduler.start()
