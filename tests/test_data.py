from datetime import date, datetime
from core.models.trade_signal import TradeSignal
import pytz

# Constants for the signal generator
BEARISH, BULLISH, NO_CLEAR_PATTERN = 1, 2, 0

moving_averages_test_cases = [
    {
        "name": "bullish",
        "ticker": "GOOGL",
        "description": "5_day_ma == 100.4, 20_day_ma == 100.1, prev_day_ma_5 == 99.8, prev_day_ma_20 == 99.95",
        "close_prices": [100 for _ in range(16)] + [99, 99, 100, 101, 103],
        "expected": TradeSignal.BULLISH
    },
    {
        "name": "bearish",
        "ticker": "AAPL",
        "description": "5_day_ma == 103, 20_day_ma == 110.5",
        "close_prices": [100 for _ in range(16)] + [102, 101, 100, 99, 97],
        "expected": TradeSignal.BEARISH
    },
    {
        "name": "bearish",
        "ticker": "MSFT",
        "description": "5_day_ma == 100, 20_day_ma == 100",
        "close_prices": [100 for _ in range(21)] ,
        "expected": TradeSignal.NO_CLEAR_PATTERN
    },
    {
        "name": "index_error",
        "ticker": "AMD",
        "description": "trigger index out of bounds exception",
        "close_prices": [100 for _ in range(21)],
        "expected": TradeSignal.NO_CLEAR_PATTERN
    }
]

engulfing_candlestick_test_cases = [
    {
        "name": "bearish",
        "open": 13,
        "close": 6,
        "previous_open": 7,
        "previous_close": 8,
        "index": ["2023-07-25", "2023-07-26"],
        "expected": TradeSignal.BEARISH
    },
    {
        "name": "bullish",
        "open": 10,
        "close": 13,
        "previous_open": 12,
        "previous_close": 11,
        "index": ["2023-07-25", "2023-07-26"],
        "expected": TradeSignal.BULLISH
    },
    {
        "name": "no clear pattern",
        "open": 11,
        "close": 12,
        "previous_open": 10,
        "previous_close": 11,
        "index": ["2023-07-25", "2023-07-26"],
        "expected": TradeSignal.NO_CLEAR_PATTERN
    }
]

alpaca_can_query_today_closing_price_test_cases = [
    {
        "name": "after_hours",
        "now": datetime(2023, 7, 27, 17, 31, tzinfo=pytz.timezone('US/Eastern')), # 5:31 PM Eastern
        "expected": True,
    },
    {
        "name": "during_hours",
        "now": datetime(2023, 7, 27, 10, 0, tzinfo=pytz.timezone('US/Eastern')), # 10 AM Eastern
        "expected": False,
    },
    {
        "name": "before_hours",
        "now": datetime(2023, 7, 27, 6, 0, tzinfo=pytz.timezone('US/Eastern')), # 10 AM Eastern
        "expected": False,
    }
]

get_first_last_market_days_test_cases = [
    {
        # Spans over week days
        "name": "over_week_dont_query_today",
        "date": date(2023, 7, 28), # Friday
        "market_days_period": 5,
        "query_today": False,
        "expected_start_date": '2023-07-21T00:00:00-04:00',
        "expected_end_date": "2023-07-27T16:30:00-04:00"
    },
    {
        # Spans over week days
        "name": "over_week_query_today",
        "date": date(2023, 7, 28), # Friday
        "market_days_period": 5,
        "query_today": True,
        "expected_start_date": '2023-07-24T00:00:00-04:00',
        "expected_end_date": "2023-07-28T16:30:00-04:00"
    },
    {
        # Spans over a weekend
        "name": "over_weekend_query_today",
        "date": date(2023, 7, 31), # Monday
        "market_days_period": 2,
        "query_today": True,
        "expected_start_date": '2023-07-28T00:00:00-04:00',
        "expected_end_date": "2023-07-31T16:30:00-04:00"
    },
    {
        # Spans over a weekend
        "name": "over_weekend_dont_query_today",
        "date": date(2023, 7, 31), # Monday
        "market_days_period": 2,
        "query_today": False,
        "expected_start_date": '2023-07-27T00:00:00-04:00',
        "expected_end_date": "2023-07-28T16:30:00-04:00"
    },
    {
        # Is weekend
        "name": "is_weekend_query_today",
        "date": date(2023, 7, 30), # Monday
        "market_days_period": 2,
        "query_today": True,
        "expected_start_date": '2023-07-27T00:00:00-04:00',
        "expected_end_date": "2023-07-28T16:30:00-04:00"
    },
    {
        # Is weekend
        "name": "is_weekend_dont_query_today",
        "date": date(2023, 7, 30), # Monday
        "market_days_period": 2,
        "query_today": False,
        "expected_start_date": '2023-07-27T00:00:00-04:00',
        "expected_end_date": "2023-07-28T16:30:00-04:00"
    },
    {
        # Spans over a holidays
        "name": "over_holiday_dont_query_today",
        "date": date(2023, 7, 7), # July 7th through July 4th
        "market_days_period": 5,
        "query_today": False,
        "expected_start_date": '2023-06-29T00:00:00-04:00',
        "expected_end_date": "2023-07-06T16:30:00-04:00"
    },
    {
        # Spans over a holidays
        "name": "over_holiday_query_today",
        "date": date(2023, 7, 7), # July 7th through July 4th
        "market_days_period": 5,
        "query_today": True,
        "expected_start_date": '2023-06-30T00:00:00-04:00',
        "expected_end_date": "2023-07-07T16:30:00-04:00"
    },
]
