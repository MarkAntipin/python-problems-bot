import random
import typing as tp
from datetime import UTC, datetime, time

from telegram.ext import ContextTypes


async def _add_daily_task_to_queue(
    context: ContextTypes.DEFAULT_TYPE,
    task: tp.Callable,
    run_at: time,
    job_name: str,
    chat_id: int,
    data: tp.Any | None = None
) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    if current_jobs:
        return False

    context.job_queue.run_daily(
        callback=task,
        time=run_at,
        chat_id=chat_id,
        name=job_name,
        data=data,
        job_kwargs={'replace_existing': True}
    )
    return True


async def create_send_questions_task(
        context: ContextTypes.DEFAULT_TYPE, task: tp.Callable, chat_id: int, user_id: int
) -> bool:
    current_time = datetime.now(UTC)
    random_minute = random.randint(0, 10)
    random_second = random.randint(0, 59)
    run_at = current_time.replace(hour=7, minute=random_minute, second=random_second).time()

    is_added = await _add_daily_task_to_queue(
        context=context,
        task=task,
        job_name=f'daily_question_{chat_id}',
        chat_id=chat_id,
        run_at=run_at,
        data=user_id
    )
    return is_added
