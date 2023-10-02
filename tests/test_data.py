from trade_bot.trading import BEARISH, BULLISH, NO_CLEAR_PATTERN


moving_averages_test_cases = [
    {
        "name": "bullish",
        "ticker": "GOOGL",
        "description": "5_day_ma == 100.4, 20_day_ma == 100.1, prev_day_ma_5 == 99.8, prev_day_ma_20 == 99.95",
        "close_prices": [100 for _ in range(16)] + [99, 99, 100, 101, 103],
        "expected": BULLISH
    },
    {
        "name": "bearish",
        "ticker": "AAPL",
        "description": "5_day_ma == 103, 20_day_ma == 110.5",
        "close_prices": [100 for _ in range(16)] + [102, 101, 100, 99, 97],
        "expected": BEARISH
    },
    {
        "name": "bearish",
        "ticker": "MSFT",
        "description": "5_day_ma == 100, 20_day_ma == 100",
        "close_prices": [100 for _ in range(21)] ,
        "expected": NO_CLEAR_PATTERN
    },
    {
        "name": "index_error",
        "ticker": "AMD",
        "description": "trigger index out of bounds exception",
        "close_prices": [100 for _ in range(21)],
        "expected": NO_CLEAR_PATTERN
    }
]
