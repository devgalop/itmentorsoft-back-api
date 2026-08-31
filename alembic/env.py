import asyncio
from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Import Base from the PostgreSQL infrastructure layer for autogenerate support.
from src.infrastructure.database.postgresql.shared.postgresql_database_session import (
    Base,
)
from src.infrastructure.database.postgresql.models import (
    AssessmentEntity,
    AssessmentAnswerEntity,
    AssessmentQuizEntity,
    AssessmentQualificationEntity,
    ClassificationResultEntity,
    ContentRating,
    QuestionEntity,
    QuestionRubricScoreEntity,
    QuestionReviewEntity,
    ResourceContentEntity,
    UserEntity,
    RoleEntity,
    RecoveryTokenEntity,
    RefreshTokenEntity,
)
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url with DATABASE_URL from environment.
# The alembic.ini placeholder is replaced at runtime.
database_url = EnvironmentVariablesConstants.DATABASE_URL
if database_url:
    # Escape '%' because ConfigParser treats it as interpolation syntax.
    escaped_database_url = database_url.replace("%", "%%")
    config.set_main_option("sqlalchemy.url", escaped_database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
