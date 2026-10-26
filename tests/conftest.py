import os
import tempfile
from collections.abc import AsyncIterator
from pathlib import Path

# URL тестовой БД (SQLite) задаётся ДО импорта app.config,
# который читает DATABASE_URL из окружения в момент импорта.
_TEST_DIR = Path(tempfile.mkdtemp(prefix="todolist-tests-"))
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{(_TEST_DIR / 'test.db').as_posix()}"

import pytest  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app as fastapi_app  # noqa: E402
from app.models import task as task_model  # noqa: F401, E402


@pytest.fixture(autouse=True)
async def prepare_database() -> AsyncIterator[None]:
    """Перед каждым тестом пересоздаём схему БД."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
