import asyncio
import os
from logging.config import fileConfig
from typing import Any, Union

from alembic import context
from asyncpg import Connection
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config
from app.config.env import env
from app.config.database.db import Base

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging. This line sets up loggers.
if config.config_file_name:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
target_metadata = Base.metadata


def get_url() -> str:
    """Retrieve the database URL from environment variables."""
    url = env['database_url']
    if not url:
        raise ValueError("DATABASE_URL environment variable is not set.")
    return url


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well. By skipping the Engine creation,
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the script output.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Union[Connection, Any]) -> None:
    """
    Perform migrations using a provided connection.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    In this scenario, we need to create an Engine
    and associate a connection with the context.
    """
    try:
        # Read the configuration section
        configuration = config.get_section(config.config_ini_section)
        if configuration is None:
            raise ValueError("Alembic configuration section is missing.")

        # Set the sqlalchemy URL from the environment
        configuration["sqlalchemy.url"] = get_url()

        # Create async engine
        connectable: AsyncEngine = async_engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        # Connect and run migrations
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    except Exception as e:
        print(f"Error running migrations: {e}")
        raise

    finally:
        # Ensure the engine is disposed of
        if 'connectable' in locals():
            await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
