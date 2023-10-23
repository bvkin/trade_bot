from alpaca_trade_manager import AlpacaTradeManager
from apscheduler.schedulers.blocking import BlockingScheduler
import google.cloud.pubsub as pubsub
import datetime
from dotenv import load_dotenv
import logging
import os
from trading import make_orders, get_first_last_market_days

import json
import random
import sys
import time

# Set global logging level to INFO
logging.basicConfig(level=logging.INFO)

# Get the logger for 'apscheduler.scheduler' and set its level to WARNING
apscheduler_logger = logging.getLogger('apscheduler.scheduler')
apscheduler_logger.setLevel(logging.WARNING)


# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
# Retrieve User-defined env vars
SLEEP_MS = os.getenv("SLEEP_MS", 0)
FAIL_RATE = os.getenv("FAIL_RATE", 0)


# Define main script
def main(sleep_ms=0, fail_rate=0):
    """Program that simulates work using the sleep method and random failures.

    Args:
        sleep_ms: number of milliseconds to sleep
        fail_rate: rate of simulated errors
    """
    print(f"Starting Task #trade-bot, Attempt #{TASK_ATTEMPT}...")
    # Simulate work by waiting for a specific amount of time
    time.sleep(float(sleep_ms) / 1000)  # Convert to seconds
    load_dotenv()

    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    trade_manager = AlpacaTradeManager(alpaca_api_key=api_key, alpaca_secret_key=secret_key)

    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path('my-project-id', 'my-topic-name')

    logging.info("Running order scheduler...")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scheduler = BlockingScheduler()
    make_orders(trade_manager, publisher,  topic_path)
    # scheduler.add_job(make_orders, 'cron', args=[trade_manager, publisher, topic_path], start_date=current_time, day_of_week='mon-fri', hour=16, minute=38, timezone='US/Eastern')
    # scheduler.start()

    # Simulate errors
    random_failure(float(fail_rate))

    print(f"Completed Task #{TASK_INDEX}.")


def random_failure(rate):
    """Throws an error based on fail rate

    Args:
        rate: an integer between 0 and 1
    """
    if rate < 0 or rate > 1:
        # Return without retrying the Job Task
        print(
            f"Invalid FAIL_RATE env var value: {rate}. "
            + "Must be a float between 0 and 1 inclusive."
        )
        return

    random_failure = random.random()
    if random_failure < rate:
        raise Exception("Task failed.")


# Start script
if __name__ == "__main__":
    try:
        main(SLEEP_MS, FAIL_RATE)
    except Exception as err:
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print(json.dumps({"message": message, "severity": "ERROR"}))
        sys.exit(1)  # Retry Job Task by exiting the process

