import pytest
from unittest.mock import call, MagicMock, patch
from trade_bot.trading import make_orders, BEARISH, BULLISH, NO_CLEAR_PATTERN

@pytest.fixture
def mock_trade_manager():
    mock = MagicMock()
    mock.get_owned_tickers.return_value = ["AAPL"]
    mock.get_price_data.return_value = MagicMock()
    return mock

@pytest.fixture
def mock_sns_client():
    return MagicMock()

@patch("trade_bot.trading.tickers_sp500", return_value=["GOOGL"])
@patch("trade_bot.trading.moving_average_signal_generator", side_effect=[BULLISH, BEARISH])
@patch("trade_bot.trading.get_first_last_market_days", return_value=("2023-01-01", "2023-01-21"))
def test_make_orders(mock_get_days, mock_signal_generator, mock_tickers_sp500, mock_trade_manager, mock_sns_client):

    mock_sns_topic_arn = "arn:aws:sns:us-east-1:123456789101:trade_bot_signals"
    make_orders(trade_manager=mock_trade_manager, sns_client=mock_sns_client, sns_topic_arn=mock_sns_topic_arn)
    
    # Ensure buy_stock was called for BULLISH signal
    mock_trade_manager.buy_stock.assert_called_once_with("GOOGL")
    
    # Ensure sell_stock was called for BEARISH signal
    mock_trade_manager.sell_stock.assert_called_once_with("AAPL")
    
    # Ensure SNS publish was called for both buy and sell
    mock_sns_client.publish.assert_has_calls([
        call(Message='Trade Bot Buy Orders Made: GOOGL',TopicArn=mock_sns_topic_arn),
        call(Message='Trade Bot Sell Orders Made: AAPL', TopicArn=mock_sns_topic_arn)
    ])
