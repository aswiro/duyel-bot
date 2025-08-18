# db_main.py - основной модуль для работы с базой данных
"""Основной модуль для работы с базой данных.

Этот модуль содержит класс Database, который управляет подключением к базе данных,
создает таблицы и предоставляет сессии для работы с данными.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from configs import settings
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import Base


class Database:
    """Класс для управления подключением к базе данных.

    Предоставляет методы для:
    - Инициализации подключения
    - Создания таблиц
    - Получения сессий
    - Закрытия подключения
    """

    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None
        self._initialized = False

    async def initialize(self, db_url: str | None = None) -> None:
        """Инициализирует подключение к базе данных."""
        if self._initialized:
            logger.warning("База данных уже инициализирована")
            return

        try:
            db_url = db_url or settings.database_url
            # Создаем движок базы данных
            engine_args = {
                "echo": settings.database_echo and "sqlite" not in db_url,
            }
            if "sqlite" not in db_url:
                engine_args.update({
                    "pool_size": settings.pool_size,
                    "max_overflow": settings.max_overflow,
                    "pool_timeout": settings.pool_timeout,
                    "pool_recycle": settings.pool_recycle,
                    "connect_args": {
                        "server_settings": {
                            "jit": "off",
                        },
                    },
                })
            self.engine = create_async_engine(db_url, **engine_args)

            # Создаем фабрику сессий
            self.session_factory = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

            # Проверяем подключение
            await self._check_connection()

            # Устанавливаем statement_timeout через отдельный SQL-запрос (только для postgres)
            if "sqlite" not in db_url:
                async with self.engine.begin() as conn:
                    await conn.execute(
                        text(f"SET statement_timeout = {settings.query_timeout}")
                    )

            self._initialized = True
            logger.info("База данных успешно инициализирована")

        except Exception as e:
            logger.error(f"Ошибка при инициализации базы данных: {e}")
            raise

    async def _check_connection(self) -> None:
        """Проверяет подключение к базе данных."""
        if not self.engine:
            raise RuntimeError("Движок базы данных не инициализирован")

        try:
            async with self.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Подключение к базе данных успешно")
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise

    async def create_tables(self) -> None:
        """Создает все таблицы в базе данных."""
        if not self.engine:
            raise RuntimeError("База данных не инициализирована")

        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all, checkfirst=True)

            logger.info("Таблицы базы данных созданы")
        except Exception as e:
            logger.error(f"Ошибка при создании таблиц: {e}")
            raise

    async def drop_tables(self) -> None:
        """Удаляет все таблицы из базы данных."""
        if not self.engine:
            raise RuntimeError("База данных не инициализирована")

        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

            logger.info("Таблицы базы данных удалены")
        except Exception as e:
            logger.error(f"Ошибка при удалении таблиц: {e}")
            raise

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Возвращает сессию базы данных в контекстном менеджере.

        Yields:
            AsyncSession: Сессия для работы с базой данных

        Raises:
            RuntimeError: Если база данных не инициализирована
        """
        if not self.session_factory:
            raise RuntimeError("База данных не инициализирована")

        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Ошибка в сессии базы данных: {e}")
                raise
            finally:
                await session.close()

    async def close(self) -> None:
        """Закрывает подключение к базе данных."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Подключение к базе данных закрыто")

        self._initialized = False
        self.engine = None
        self.session_factory = None

    async def init_db(self) -> None:
        """Полная инициализация базы данных: подключение + создание таблиц."""
        await self.initialize()
        await self.create_tables()
        logger.info("База данных полностью инициализирована")

    @property
    def is_initialized(self) -> bool:
        """Проверяет, инициализирована ли база данных."""
        return self._initialized
