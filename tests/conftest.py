import asyncio
import pytest
import pytest_asyncio

from database.core import Database
from database.unit_of_work import UnitOfWork

# Используем SQLite в памяти для тестов
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Создает экземпляр event loop для всего тестового сеанса."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db() -> Database:
    """
    Фикстура для предоставления экземпляра Database,
    инициализированного с тестовой базой данных.
    """
    db_instance = Database()
    await db_instance.initialize(db_url=TEST_DATABASE_URL)
    await db_instance.create_tables()
    yield db_instance
    await db_instance.drop_tables()
    await db_instance.close()


@pytest_asyncio.fixture(scope="function")
async def test_uow(db: Database) -> UnitOfWork:
    """
    Главная фикстура, предоставляющая UnitOfWork для тестовой сессии.
    """
    async with db.get_session() as session:
        yield UnitOfWork(session)
