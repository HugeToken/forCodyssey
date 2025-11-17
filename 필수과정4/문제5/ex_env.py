# alembic/env.py (전체 대체 코드)
import asyncio
from logging.config import fileConfig

from models import Base
from database import engine 

from alembic import context
target_metadata = Base.metadata


def do_run_migrations(connection):
    """마이그레이션 스크립트를 실행합니다."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations(connectable):
    """💡 비동기 연결을 처리합니다. (수정된 run_sync 호출 방식)"""
    async with connectable.begin() as connection:
        await connection.run_sync(
            do_run_migrations,
        )


def run_migrations_online() -> None:
    """💡 Run migrations in 'online' mode (비동기 방식으로 변경)."""
    
    connectable = engine 

    asyncio.run(run_async_migrations(connectable))


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()