from core.utils.trading_calculators import calculate_bid_ask_spread
import unittest

class TestTradingCalculators(unittest.TestCase):
    def test_calculate_bid_ask_spread(self):
        # ask_price > bid_price
        bid_ask_spread = calculate_bid_ask_spread(bid_price=148.86, ask_price=149.07)
        self.assertAlmostEqual(bid_ask_spread, 0.21, places=2)

        # bid_price > ask_price
        self.assertRaises(ValueError, calculate_bid_ask_spread, bid_price=149.07, ask_price=148.86)

if __name__ == '__main__':
    unittest.main()
