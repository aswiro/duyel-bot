from aiogram import Dispatcher

from .main import router

from .dialogs import main_dialog, game_room_dialog


async def dialogs_init(dp: Dispatcher) -> None:
    """Регистрация всех диалогов."""
    dp.include_routers(main_dialog, game_room_dialog)


async def routers_init(dp: Dispatcher):
    """Include all routers in the dispatcher."""
    dp.include_router(router)


__all__ = [
    "dialogs_init",
    "routers_init",
]
