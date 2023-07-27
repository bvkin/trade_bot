import datetime
import unittest
from trade_bot.alpaca_trade_manager import AlpacaTradeManager

class TestAlpacaTradeManager(unittest.TestCase):

    def test__get_date_range(self):
        atm = AlpacaTradeManager()

        # If today is Monday (weekday = 0)
        today = datetime.date(2023, 8, 7)
        self.assertEqual(atm._get_date_range(today), (datetime.date(2023, 8, 3), datetime.date(2023, 8, 4)))

        # If today is Tuesday (weekday = 1)
        today = datetime.date(2023, 8, 8)
        self.assertEqual(atm._get_date_range(today), (datetime.date(2023, 8, 4), datetime.date(2023, 8, 7)))

        # If today is some other day (e.g., Wednesday)
        today = datetime.date(2023, 8, 9)
        self.assertEqual(atm._get_date_range(today), (datetime.date(2023, 8, 7), datetime.date(2023, 8, 8)))

if __name__ == '__main__':
    unittest.main()
