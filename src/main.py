from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

from trading import make_orders


if __name__ == '__main__':
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scheduler = BlockingScheduler()
    scheduler.add_job(make_orders, 'cron', start_date=current_time, day_of_week='mon-fri',hour=9, timezone='US/Eastern')
    print("running order scheduler...")
    scheduler.start()
