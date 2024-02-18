from core.alpaca.alpaca_trade_manager import AlpacaTradeManager
from core.trading.strategy import Strategy
from boto3_type_annotations.sns import Client as SNSClient
from core.utils.market_time import get_market_day_range
import pandas as pd
from typing import Tuple
from talib import ATR
import sys
import os

def calculate_purchase_amnt(buying_power: float, buying_percentage: float) -> float:
    # get buying power
    buying_percentage = os.getenv('BUYING_PERCENTAGE')
    # calculate buying percentage
    return buying_percentage * buying_power

def calculate_sl_tp(purchase_amnt: float, sltp_multiplier: float, df:pd.DataFrame) -> Tuple:
    # get entry price
    
    atr = ATR(df['high'], df['low'], df['close'], timeperiod=14)
    atr = df.iloc[-1]
    stop_loss = atr * sltp_multiplier
    take_profit = atr * sltp_multiplier
        
    return [stop_loss, take_profit]
