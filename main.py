import asyncio

from loguru import logger

from configs import (
    setup_bot_logger,
    # setup_logger,
    get_logger,
)
from core.bot import bot_init
from core.db import (
    close_database,
    init_database,
    redis_init,
)


async def main():
    # setup_logger()
    setup_bot_logger()
    get_logger("aiogram")

    await init_database()
    await redis_init()
    try:
        await bot_init()
    finally:
        await close_database()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
