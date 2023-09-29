import asyncio
from datetime import UTC

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.utils.postgres_pool import pg_pool
from tasks.send_questions import send_daily_questions_task


def main() -> None:
    scheduler = AsyncIOScheduler(timezone=UTC)
    scheduler.add_job(
        send_daily_questions_task,
        args=(pg_pool,),
        trigger='cron',
        day_of_week='*',
        hour=7,
        minute=0
    )
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
