from logging.config import fileConfig
import os
from sqlalchemy import pool
from alembic import context
from database.models import Base  # Импорт своей базы моделей
from sqlalchemy.ext.asyncio import create_async_engine

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata

DB_URL = os.environ.get('DATABASE_URL')

def run_migrations_online():
    connectable = create_async_engine(DB_URL, poolclass=pool.NullPool)

    async def do_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(
                lambda sync_conn: context.configure(
                    connection=sync_conn,
                    target_metadata=target_metadata,
                    compare_type=True,
                )
            )
            await connection.run_sync(lambda sync_conn: context.run_migrations())

    import asyncio
    asyncio.run(do_migrations())


run_migrations_online()