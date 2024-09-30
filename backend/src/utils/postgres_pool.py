import asyncio

import asyncpg

from settings import PostgresSettings


async def get_pg_pool() -> asyncpg.Pool:
    pg_settings = PostgresSettings()
    return await asyncpg.create_pool(dsn=pg_settings.url)

loop = asyncio.get_event_loop()
pg_pool = loop.run_until_complete(get_pg_pool())
