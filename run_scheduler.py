import asyncio
import logging
import pytz

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.utils.postgres_pool import pg_pool
from tasks.send_questions import send_daily_questions_task
from tasks.send_advices import send_advices_task

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('ptbcontrib').setLevel(logging.WARNING)


def main() -> None:
    scheduler = AsyncIOScheduler(timezone=pytz.utc)
    scheduler.add_job(
        send_daily_questions_task,
        args=(pg_pool,),
        trigger='cron',
        day_of_week='*',
        hour=7,
        minute=0
    )
    scheduler.add_job(
        send_advices_task,
        args=(pg_pool,),
        trigger=IntervalTrigger(days=3),
        day_of_week='*',
        hour=10,
        minute=0
    )
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
