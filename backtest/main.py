import sys
sys.path.append('..')

from backtesting import Backtest
from dotenv import load_dotenv
import os
import pandas as pd
from trading_strategy import TadingStrategy
from trade_bot.alpaca_trade_manager import AlpacaTradeManager 
from trade_bot.trading import moving_average_signal_generator


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    trade_manager = AlpacaTradeManager(alpaca_api_key=api_key, alpaca_secret_key=secret_key)

    # Get price data for chosen stock
    df = trade_manager.get_price_data('AMD', '2015-12-01', '2022-12-31')

    # Add buy/sell signals to dataframe
    signal = [0] * len(df)
    back_avg = 21
    for row in range(back_avg, len(df)):
        row_start = row - back_avg
        signal[row] = moving_average_signal_generator(df.iloc[row_start:row].copy())
    df['signal']=signal

    # Format dataframe to conform with backtesting library
    df.drop(columns=['trade_count', 'vwap'], inplace=True)
    df = df.reset_index()
    df.columns = ['Local time', 'Open', 'High', 'Low', 'Close', 'Volume', 'signal']
    df['Local time'] = pd.to_datetime(df['Local time'])

    # Backtest
    bt = Backtest(df, TadingStrategy, cash=1_000, commission=.002)
    stat = bt.run()
    print(stat)
    bt.plot()
