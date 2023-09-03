import random
import typing as tp
from datetime import UTC, datetime, time

from telegram.ext import ContextTypes

from settings import MOSCOW_TIME_DIFFERENCE


async def _add_daily_task_to_queue(
    context: ContextTypes.DEFAULT_TYPE,
    task: tp.Callable,
    run_at: time,
    job_name: str,
    chat_id: int,
    data: tp.Any | None = None
) -> None:
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    if current_jobs:
        return

    context.job_queue.run_daily(
        callback=task,
        time=run_at,
        chat_id=chat_id,
        name=job_name,
        data=data,
        job_kwargs={'replace_existing': True}
    )


async def create_send_questions_task(
        context: ContextTypes.DEFAULT_TYPE, task: tp.Callable, chat_id: int, user_id: int
) -> None:
    current_moscow_time = datetime.now(UTC) + MOSCOW_TIME_DIFFERENCE
    random_minute = random.randint(0, 10)
    random_second = random.randint(0, 59)
    run_at = current_moscow_time.replace(hour=10, minute=random_minute, second=random_second).time()

    await _add_daily_task_to_queue(
        context=context,
        task=task,
        job_name=f'daily_question_{chat_id}',
        chat_id=chat_id,
        run_at=run_at,
        data=user_id
    )
