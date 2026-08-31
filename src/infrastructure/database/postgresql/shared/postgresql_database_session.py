from urllib.parse import urlparse, urlunparse

import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants


def _get_database_name(url: str) -> str:
    """Extract database name from connection URL."""
    parsed = urlparse(url)
    return parsed.path.lstrip("/")


def _get_admin_url(url: str) -> str:
    """Create admin URL pointing to 'postgres' database.

    Strips the SQLAlchemy driver suffix (+asyncpg) since asyncpg.connect()
    only accepts 'postgresql://' or 'postgres://' schemes.
    """
    parsed = urlparse(url)
    # Remove driver suffix: postgresql+asyncpg -> postgresql
    scheme = parsed.scheme.split("+")[0]
    admin_parsed = parsed._replace(path="/postgres", scheme=scheme)
    return urlunparse(admin_parsed)


async def ensure_database_exists():
    """Ensure the target database exists, create it if it doesn't."""
    db_name = _get_database_name(EnvironmentVariablesConstants.DATABASE_URL)
    admin_url = _get_admin_url(EnvironmentVariablesConstants.DATABASE_URL)

    conn = await asyncpg.connect(admin_url)
    try:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", db_name
        )
        if not exists:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Database '{db_name}' created successfully")
    finally:
        await conn.close()


engine = create_async_engine(
    EnvironmentVariablesConstants.DATABASE_URL,
    pool_size=int(EnvironmentVariablesConstants.DB_POOL_SIZE),
    max_overflow=int(EnvironmentVariablesConstants.DB_MAX_OVERFLOW),
    pool_timeout=int(EnvironmentVariablesConstants.DB_POOL_TIMEOUT),
    pool_pre_ping=True,
    pool_recycle=int(EnvironmentVariablesConstants.DB_POOL_RECYCLE),
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    """Initialize database by creating all tables.

    For production, run migrations via CLI: alembic upgrade head
    This method uses create_all for development/convenience.
    """
    await ensure_database_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
