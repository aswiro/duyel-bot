from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from loguru import logger

from database import Database, UnitOfWork
import configs as settings
from cache import RedisClient

db = Database()
rc = RedisClient()


async def redis_init():
    try:
        # Инициализация Redis
        await rc.connect()
        logger.info("Redis initialized")
    except Exception as e:
        logger.error(f"Redis initialization failed: {e}")


async def init_database() -> None:
    """Инициализирует базу данных и создает таблицы при запуске приложения."""
    try:
        await db.initialize()
        await db.create_tables()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")


async def close_database() -> None:
    """Закрывает подключение к базе данных при завершении приложения."""
    try:
        await db.close()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Database closure failed: {e}")


async def load_admin_list():
    """Загружает и обновляет список администраторов бота."""

    async with db.get_session() as session:
        uow = UnitOfWork(session)
        async with uow:
            admin_ids = await uow.group_service.get_all_admin_ids()
            settings.bot_admin_ids = admin_ids
    logger.info(f"Admin list loaded: {settings.bot_admin_ids}")


def get_storage() -> RedisStorage:
    """Возвращает инициализированное хранилище Redis."""
    if not rc.redis:
        raise ConnectionError("Redis client is not initialized")
    return RedisStorage(rc.redis, key_builder=DefaultKeyBuilder(with_destiny=True))


async def delete_tables():
    """Удаляет все таблицы в базе данных."""
    await db.drop_tables()
    logger.info("All tables deleted")
