from datetime import datetime, date, time, timedelta
import pandas_market_calendars as mcal
import pytz
from typing import Tuple

def get_market_day_range(market_days_period: int) -> Tuple[str, str]:
    """
    Returns a period of market days based on todays date

    Parameters:
        market_days_period (int): Number of days a market period should span, based on the current date

    Returns:
        period_start (str): An RFC-3339 string representing the start date of the period
        period_end (str): An RFC-3339 string representing the end of the period. Time is rutruned as after 4PM (eastern) if the market is done trading for the day.

    """

    # Check if it is safe to include today in time frame
    query_today = alpaca_can_query_today_closing_price()

    # Get the NYSE calendar
    nyse = mcal.get_calendar('NYSE')

    # Get today in datetime format
    today = datetime.combine(date.today(), time(0, 0))

    # Subtract 1 day if query_today=False
    offset_day = lambda x: 0 if x else 1
    end_date = today - timedelta(days=offset_day(query_today))
    start_date = end_date - timedelta(days=(market_days_period)*3)  # Assuming weekends and holidays, approx n*3 should cover it

    # Get period start and end dates
    market_days = nyse.valid_days(start_date=start_date, end_date=end_date)[-market_days_period:]
    period_start = datetime.combine(market_days[0], time(0, 0)).strftime('%Y-%m-%dT%H:%M:%S-04:00')
    period_end = datetime.combine(market_days[-1], time(16, 30)).strftime('%Y-%m-%dT%H:%M:%S-04:00')

    return period_start, period_end


def alpaca_can_query_today_closing_price() -> bool:
    """
    Checks if the closing price of the day is safe to query on alpaca api 

    Returns:
        query_today (bool): True if the current time is after 4:16 PM (can query for todays closing price on alpaca free tier)
            else False
    """
    current_time = datetime.now(pytz.timezone('US/Eastern'))

    # Define the cutoff time as 16:16 (4:16 PM)
    cutoff_time = datetime.strptime("16:16", "%H:%M").time()

    query_today = current_time.time() >= cutoff_time

    return query_today
