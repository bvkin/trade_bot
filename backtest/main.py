import sys
sys.path.append('..')

import argparse
from backtesting import Backtest
import datetime
from dotenv import load_dotenv
import os
import pandas as pd
from trading_strategy import TradingStrategy
from core.alpaca.alpaca_trade_manager import AlpacaTradeManager
from trade_bot.trading import moving_average_signal_generator


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Backtest a given stock over a given period")
    parser.add_argument("ticker", help="Stock ticker to perform backtesting on")
    parser.add_argument("period", default=3, help="Period in years for which to pull data for backtesting")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    trade_manager = AlpacaTradeManager(alpaca_api_key=api_key, alpaca_secret_key=secret_key)

    # Calculate dates to pull data for backtest
    today = datetime.date.today()
    end_period = today - datetime.timedelta(days=1)
    start_period = end_period.replace(year=today.year - int(args.period))

    df = trade_manager.get_price_data(args.ticker, start_period.strftime("%Y-%m-%d"), end_period.strftime("%Y-%m-%d"), adjustment='split')

    # Add buy/sell signals to dataframe
    signal = [0] * len(df)
    back_avg = 21
    for row in range(back_avg, len(df)):
        row_start = row - back_avg
        signal[row] = moving_average_signal_generator(df.close[row_start:row]).value
    df['signal']=signal

    # Format dataframe to conform with backtesting library
    df.drop(columns=['trade_count', 'vwap'], inplace=True)

    # Reformat dataframe index
    df = df.reset_index()
    df.rename(columns={'timestamp': 'dates'}, inplace=True)
    df['dates'] =  pd.to_datetime(df['dates'].dt.date)
    df = df.set_index('dates')

    # Set column names to backtest standard
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'signal']

    # Backtest
    bt = Backtest(df, TradingStrategy, cash=10_000, commission=.002)
    stat = bt.run()
    print(stat)

    # Graph
    if not os.path.exists("graphs"):
        os.mkdir("graphs")

    bt.plot(
        filename=f'graphs/{args.ticker}-{args.period}.html',
    )
