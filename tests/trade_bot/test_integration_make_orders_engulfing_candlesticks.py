from core.trading.engulfing_candlesticks import EngulfingCandlesticks
from pandas import DataFrame
import pytest
from unittest.mock import call, MagicMock, patch
from tests.test_data import engulfing_candlestick_test_cases
from trade_bot.make_orders import make_orders

tickers = [case["ticker"] for case in engulfing_candlestick_test_cases]


def price_data_generator(values):
    """
    Generates a fresh dataframe each time called for mocking
    """
    while True:
        for value in values:
            df = DataFrame({
                "open" : [100, value["prev_open"], value["open"]],
                "high" : [100, value["prev_high"], value["high"]],
                "low"  : [100, value["prev_low"], value["low"]],
                "close": [100, value["prev_close"], value["close"]]
            })
            yield df

@pytest.fixture
def mock_trade_manager():
    mock = MagicMock()
    mock.get_owned_tickers.return_value = tickers
    mock.get_price_data.side_effect = price_data_generator(engulfing_candlestick_test_cases)
    return mock

@pytest.fixture
def mock_sns_client():
    return MagicMock()

@patch("core.utils.market_time.get_market_day_range", return_value=("2023-01-01", "2023-01-21"))
def test_make_orders_engulfing_candlesticks(mock_get_market_day_range, mock_trade_manager, mock_sns_client):
    mock_sns_topic_arn = "arn:aws:sns:us-east-1:123456789101:trade_bot_signals"

    make_orders(trade_manager=mock_trade_manager, Strategy=EngulfingCandlesticks, tickers=tickers, sns_client=mock_sns_client, sns_topic_arn=mock_sns_topic_arn)

    # Ensure buy_stock was called for BULLISH signal
    mock_trade_manager.buy_stock.assert_called_once_with("AAPL")
    
    # Ensure sell_stock was called for BEARISH signal
    mock_trade_manager.sell_stock.assert_called_once_with("GOOGL")

    # Ensure SNS publish was called for both buy and sell
    mock_sns_client.publish.assert_has_calls([
        call(Message='Trade Bot Buy Orders Made: AAPL',TopicArn=mock_sns_topic_arn),
        call(Message='Trade Bot Sell Orders Made: GOOGL', TopicArn=mock_sns_topic_arn)
    ])
