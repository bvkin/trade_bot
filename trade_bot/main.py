from trade_bot.alpaca_trade_manager import AlpacaTradeManager
from apscheduler.schedulers.blocking import BlockingScheduler
import boto3
import datetime
from dotenv import load_dotenv
import logging
import os
from trading import make_orders

# Set global logging level to INFO
logging.basicConfig(level=logging.INFO)

# Get the logger for 'apscheduler.scheduler' and set its level to WARNING
apscheduler_logger = logging.getLogger('apscheduler.scheduler')
apscheduler_logger.setLevel(logging.WARNING)

if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    trade_manager = AlpacaTradeManager(alpaca_api_key=api_key, alpaca_secret_key=secret_key)

    aws_region = os.getenv('AWS_DEFAULT_REGION')
    sns_topic_arn = os.getenv('AWS_SNS_TOPIC_ARN')
    sns_client = boto3.client("sns", region_name=aws_region)

    tickers = os.getenv('TICKERS').split(',')

    logging.info("Running order scheduler...")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scheduler = BlockingScheduler()
    scheduler.add_job(make_orders, 'cron', args=[trade_manager, tickers, sns_client, sns_topic_arn], start_date=current_time, day_of_week='mon-fri',hour=9, timezone='US/Eastern')
    scheduler.start()
