from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from loguru import logger

from .states import DuelSG

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    """Универсальный обработчик команды /start"""
    # Clear any existing dialog state
    await dialog_manager.reset_stack()

    # Запускаем объединенный диалог, который автоматически определит тип пользователя
    logger.debug("Start Main Menu")
    await dialog_manager.start(DuelSG.main_menu, mode=StartMode.RESET_STACK)
