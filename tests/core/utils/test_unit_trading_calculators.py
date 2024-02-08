import unittest
from unittest.mock import patch
from core.alpaca.alpaca_trade_manager import AlpacaTradeManager
from core.trading.strategy import Strategy
from boto3_type_annotations.sns import Client as SNSClient
from core.utils.market_time import get_market_day_range
from core.utils.trading_calculators import calculate_purchase_amnt, calculate_sl_tp
# from datetime import date, datetime
import pandas as pd
from typing import Tuple
from talib import ATR
import os

class TestTradingCalculators(unittest.TestCase):
    def test_calculate_purchase_amnt(self):
        # mock_datetime.now.return_value = datetime(2024, 2, 2, 12, 0)  # Set a specific datetime for testing
        # mock_date.today.return_value = date(2024, 2, 2)  # Set a specific date for testing

        # Mock the environment variable
        with patch.dict(os.environ, {'BUYING_PERCENTAGE': '0.5'}):
            buying_power = 10000.0
            buying_percentage = float(os.getenv('BUYING_PERCENTAGE'))
            result = calculate_purchase_amnt(buying_power, buying_percentage)
            self.assertEqual(result, 5000.0)

    def test_calculate_sl_tp(self):
        df = pd.DataFrame({
            'high': [120.0, 130.0, 110.0],
            'low': [100.0, 110.0, 90.0],
            'close': [110.0, 120.0, 100.0],
        })

        purchase_amnt = 5000.0
        sltp_multiplier = 2.0

        mock_atr = ATR(df['high'], df['low'], df['close'], timeperiod=14)
        mock_atr = mock_atr.iloc[-1]
        #mock_atr.return_value = [15.0, 20.0, 10.0]  # Mock ATR values for testing
        result = calculate_sl_tp(purchase_amnt, sltp_multiplier, df)
        # (30.0, 40.0)
        expected_result = (30.0, 40.0)  # Calculate based on mocked ATR values and multiplier
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()