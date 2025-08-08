from collections.abc import Awaitable, Callable
from typing import Any, Final

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

# Импортируем созданный экземпляр
from localization import fd
from database.unit_of_work import UnitOfWork
from loguru import logger


class L10nMiddleware(BaseMiddleware):
    middleware_key: Final[str] = "l10n"

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        locale = "ru"
        logger.debug(f"User Data {user}")
        if user:
            uow: UnitOfWork | None = data.get("uow")
            if uow:
                db_user = await uow.user_service.get_user(user.id)
                if db_user:
                    user = db_user
                else:
                    user = await uow.user_service.create_user(user)

                if user and user.language_code:
                    locale = user.language_code
            elif user.language_code:
                locale = user.language_code

        if locale not in ["ru", "en"]:
            locale = "ru"

        l10n = fd.get_language(locale)
        data[self.middleware_key] = l10n

        return await handler(event, data)
