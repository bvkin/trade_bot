from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import logging

from trading import make_orders

# Set global logging level to INFO
logging.basicConfig(level=logging.INFO)

# Get the logger for 'apscheduler.scheduler' and set its level to WARNING
apscheduler_logger = logging.getLogger('apscheduler.scheduler')
apscheduler_logger.setLevel(logging.WARNING)

if __name__ == '__main__':
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scheduler = BlockingScheduler()
    logging.info("Running order scheduler...")
    scheduler.add_job(make_orders, 'cron', start_date=current_time, day_of_week='mon-fri',hour=9, timezone='US/Eastern')
    scheduler.start()
