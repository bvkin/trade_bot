from core.alpaca.alpaca_trade_manager import AlpacaTradeManager
from core.trading.strategy import Strategy
from core.models.trade_signal import TradeSignal
from core.utils.market_time import get_market_day_range
from boto3_type_annotations.sns import Client as SNSClient
from typing import List
import logging


def make_orders(trade_manager: AlpacaTradeManager, Strategy: Strategy, tickers: List[str], sns_client: SNSClient,  sns_topic_arn: str = None) -> None:
    """
    Makes buy orders for all stocks in the S&P 500 given a bullish signal.
    Makes sell orders for all owned stocks bearish signal.
    """
    
    purchased_tickers, sold_tickers = [], []
    period_start, period_end = get_market_day_range(21) # 21 for 20 day moving avg
    # logging.info("[For Sale] Account Balance: " + trade_manager.api.get_account().buying_power)
    logging.info("Making orders...")
    
    owned_tickers = trade_manager.get_owned_tickers()

    for ticker in owned_tickers:
        logging.info("Evaluating " + ticker + " for sell")
        df = trade_manager.get_price_data(ticker, period_start, period_end)
        
        strat = Strategy(df)
        
        if strat.signal() == TradeSignal.BEARISH:
            trade_manager.sell_stock(ticker)
            logging.info("Sell order for " + ticker + " placed.")
            sold_tickers.append(ticker)

    if sold_tickers and sns_topic_arn != None:
        sns_client.publish(Message=f'Trade Bot Sell Orders Made: {", ".join(sold_tickers)}', TopicArn=sns_topic_arn)
    
    balance_available = trade_manager.api.get_account().buying_power
    # logging.info("[For Purchase] Account Balance: " + balance_available)
    for ticker in tickers:
        logging.info("Evaluating " + ticker + " for buy")
        df = trade_manager.get_price_data(ticker, period_start, period_end)
        strat = Strategy(df)

        if strat.signal() == TradeSignal.BULLISH:
            trade_manager.buy_stock(ticker)
            
            purchased_tickers.append(ticker)

    if purchased_tickers and sns_topic_arn != None:
        sns_client.publish(Message=f'Trade Bot Buy Orders Made: {", ".join(purchased_tickers)}', TopicArn=sns_topic_arn)
