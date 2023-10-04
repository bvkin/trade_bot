from alpaca_trade_manager import AlpacaTradeManager
from apscheduler.schedulers.blocking import BlockingScheduler
import google.cloud.pubsub as pubsub
import datetime
from dotenv import load_dotenv
import logging
import os
from trading import make_orders, get_first_last_market_days

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

    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path('my-project-id', 'my-topic-name')

    logging.info("Running order scheduler...")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scheduler = BlockingScheduler()
    scheduler.add_job(make_orders, 'cron', args=[trade_manager, publisher, topic_path], start_date=current_time, day_of_week='mon-fri', hour=14, minute=31, timezone='US/Eastern')
    scheduler.start()