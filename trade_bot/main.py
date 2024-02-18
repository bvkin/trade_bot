import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from core.alpaca.alpaca_trade_manager import AlpacaTradeManager
from core.trading.moving_averages import MovingAverages
from core.trading.engulfing_candlesticks import EngulfingCandlesticks
from core.trading.bbands_rsi import BBandsRSI
from core.trading.macd import MACD

import boto3
import datetime
from dotenv import load_dotenv
import logging
import os
from trade_bot.make_orders import make_orders

# Set global logging level to INFO
logging.basicConfig(level=logging.INFO)

# Get the logger for 'apscheduler.scheduler' and set its level to WARNING
apscheduler_logger = logging.getLogger('apscheduler.scheduler')
apscheduler_logger.setLevel(logging.WARNING)

def parse_tickers(tickers):
    return [ticker.strip() for ticker in tickers.split(',')]

if __name__ == '__main__':
    strategy_choices = {
        "BBandsRSI": BBandsRSI,
        "EngulfingCandlesticks": EngulfingCandlesticks,
        "EngulfingCandlesticks": EngulfingCandlesticks,
        "MACD": MACD,
        "MovingAverages": MovingAverages,
    }

    parser = argparse.ArgumentParser(description="Bot to automatically manage a stock portfolio")
    parser.add_argument("--strategy", choices=list(strategy_choices.keys()), help="Strategy to run")
    parser.add_argument("--tickers", type=parse_tickers, help="A comma separated list of tickers to evaluate with strategy")
    args = parser.parse_args()

    strat = strategy_choices[args.strategy]

    load_dotenv()
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    trade_manager = AlpacaTradeManager(alpaca_api_key=api_key, alpaca_secret_key=secret_key)

    aws_region = os.getenv('AWS_DEFAULT_REGION')
    sns_topic_arn = os.getenv('AWS_SNS_TOPIC_ARN')
    sns_client = boto3.client("sns", region_name=aws_region)

    logging.info("Running order scheduler...")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scheduler = BlockingScheduler()
    scheduler.add_job(make_orders, 'cron', args=[trade_manager, strat, args.tickers, sns_client, sns_topic_arn], start_date=current_time, day_of_week='mon-fri',hour=9, timezone='US/Eastern')
    scheduler.start()
