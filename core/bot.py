from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import setup_dialogs
from loguru import logger

from configs import settings
from handlers import dialogs_init, routers_init
from middlewares import DbSessionMiddleware, L10nMiddleware

from .db import db, get_storage


async def bot_init():
    # Bot
    bot = Bot(
        token=settings.telegram_bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    # Инициализация диспетчера
    storage = get_storage()
    dp = Dispatcher(storage=storage)

    # Регистрация middleware

    dp.update.middleware(DbSessionMiddleware(db))
    dp.update.middleware(L10nMiddleware())

    # Инициализация диалогов (должно быть до роутеров)
    await dialogs_init(dp)
    setup_dialogs(dp)

    # Инициализация роутеров
    await routers_init(dp)
    dp["settings"] = settings

    # Запускаем бота
    logger.info("Starting bot")
    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            skip_updates=True,
        )
    finally:
        logger.info("Bot stopped")
