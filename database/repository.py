# repository.py - базовый репозиторий для работы с данными
"""Базовый репозиторий для работы с данными.

Этот модуль содержит базовый класс Repository, который предоставляет
стандартные методы для работы с данными (CRUD операции).
"""

from typing import Any, TypeVar

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .models import (
    GameStatusEnum,
    User,
    Game,
    Roll,
    Transaction,
    WithdrawalRequest,
)

# Типы для Generic репозитория
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
FilterSchemaType = TypeVar("FilterSchemaType")


class BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType, FilterSchemaType]:
    """Базовый репозиторий для работы с моделями.

    Предоставляет стандартные CRUD операции:
    - create: создание записи
    - get: получение записи по ID
    - get_multi: получение нескольких записей
    - update: обновление записи
    - delete: удаление записи

    Args:
        model: Класс модели SQLAlchemy
        session: Сессия базы данных
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        if not hasattr(self, "model") or self.model is None:
            raise NotImplementedError("Model is not set for repository")
        self.session = session

    async def get(self, pk: Any) -> ModelType | None:
        """Получает запись по ID.

        Args:
            pk: Первичный ключ записи

        Returns:
            Найденная запись или None
        """
        try:
            # Предполагаем, что поле ID называется 'id'
            stmt = select(self.model).where(self.model.id == pk)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()

        except Exception as e:
            logger.error(f"Ошибка при получении {self.model.__name__} с ID {pk}: {e}")
            raise

    async def get_multi(
        self, skip: int = 0, limit: int = 100, filters: FilterSchemaType | None = None
    ) -> list[ModelType]:
        """Получает несколько записей с пагинацией и фильтрацией.

        Args:
            skip: Количество записей для пропуска
            limit: Максимальное количество записей
            **filters: Дополнительные фильтры

        Returns:
            Список найденных записей
        """
        try:
            stmt = select(self.model)

            # Применяем фильтры
            if filters:
                if hasattr(filters, "model_dump"):
                    filter_data = filters.model_dump(exclude_unset=True)
                elif hasattr(filters, "dict"):
                    filter_data = filters.dict(exclude_unset=True)
                else:
                    filter_data = filters

                for field, value in filter_data.items():
                    if hasattr(self.model, field) and value is not None:
                        stmt = stmt.where(getattr(self.model, field) == value)

            stmt = stmt.offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Ошибка при получении списка {self.model.__name__}: {e}")
            raise

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Создает новую запись в базе данных.

        Args:
            obj_in: Данные для создания записи

        Returns:
            Созданная запись
        """
        try:
            # Если obj_in это Pydantic модель, конвертируем в dict
            if hasattr(obj_in, "model_dump"):
                obj_data = obj_in.model_dump()
            elif hasattr(obj_in, "dict"):
                obj_data = obj_in.dict()
            else:
                obj_data = obj_in

            db_obj = self.model(**obj_data)
            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)

            logger.debug(
                f"Создана запись {self.model.__name__} с ID: {getattr(db_obj, 'id', 'N/A')}"
            )
            return db_obj

        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка при создании {self.model.__name__}: {e}")
            raise

    async def update(self, pk: Any, obj_in: UpdateSchemaType) -> ModelType | None:
        """Обновляет запись по ID.

        Args:
            pk: Первичный ключ записи
            obj_in: Данные для обновления

        Returns:
            Обновленная запись или None если не найдена
        """
        try:
            # Получаем существующую запись
            db_obj = await self.get(pk)
            if not db_obj:
                return None

            # Подготавливаем данные для обновления
            if hasattr(obj_in, "model_dump"):
                update_data = obj_in.model_dump(exclude_unset=True)
            elif hasattr(obj_in, "dict"):
                update_data = obj_in.dict(exclude_unset=True)
            else:
                update_data = obj_in

            # Обновляем поля
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            await self.session.commit()
            await self.session.refresh(db_obj)

            logger.debug(f"Обновлена запись {self.model.__name__} с ID: {pk}")
            return db_obj

        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка при обновлении {self.model.__name__} с ID {pk}: {e}")
            raise

    async def delete(self, pk: Any) -> bool:
        """Удаляет запись по ID.

        Args:
            pk: Первичный ключ записи

        Returns:
            True если запись была удалена, False если не найдена
        """
        try:
            # Проверяем существование записи
            db_obj = await self.get(pk)
            if not db_obj:
                return False

            stmt = delete(self.model).where(self.model.id == pk)
            result = await self.session.execute(stmt)
            await self.session.commit()

            deleted_count = result.rowcount
            if deleted_count > 0:
                logger.debug(f"Удалена запись {self.model.__name__} с ID: {pk}")
                return True
            return False

        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка при удалении {self.model.__name__} с ID {pk}: {e}")
            raise


# Определение конкретных репозиториев
class UserRepository(BaseRepository[User, dict, dict, dict]):
    model = User


class GameRepository(BaseRepository[Game, dict, dict, dict]):
    model = Game

    async def get_pending_games_exclude_user(self, user_id: int) -> list[Game]:
        """Получает список игр со статусом pending, где player1_id не равен user_id"""
        stmt = select(Game).where(
            Game.status == GameStatusEnum.pending,
            Game.player1_id != user_id
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class RollRepository(BaseRepository[Roll, dict, dict, dict]):
    model = Roll


class TransactionRepository(BaseRepository[Transaction, dict, dict, dict]):
    model = Transaction


class WithdrawalRequestRepository(BaseRepository[WithdrawalRequest, dict, dict, dict]):
    model = WithdrawalRequest
