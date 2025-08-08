from aiogram.types import CallbackQuery
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Column, Group
from aiogram_dialog.widgets.text import Const, Format

from configs.settings import settings
from database import UnitOfWork

from ..states import DuelSG
from ..widgets import (
    GamesWindowWidgets,
    UserDialogWidgets,
)


async def get_main_data(dialog_manager, **kwargs):
    """Получение данных для основного диалога."""

    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    l10n = dialog_manager.middleware_data["l10n"]
    user_id = dialog_manager.event.from_user.id

    async with uow:
        user = await uow.user_service.get_user(user_id)
        if user is None:
            await uow.user_service.create_user(
                dialog_manager.event.from_user,
            )

    is_admin = user_id in settings.bot_admin_ids

    return {
        "l10n": l10n,
        "is_admin": is_admin,
        "admin_name": dialog_manager.event.from_user.full_name,
        "user_name": dialog_manager.event.from_user.full_name,
        "l10n_welcome": l10n.format_value(
            "admin-welcome-message" if is_admin else "welcome-message"
        ).format(user_name=dialog_manager.event.from_user.full_name),
        "l10n_games_menu": l10n.format_value("games-menu"),
        "l10n_change_language": l10n.format_value("change-language"),
        "l10n_support": l10n.format_value("support"),
        "l10n_choose_language": l10n.format_value("choose-language"),
    }


async def on_admin_action(callback: CallbackQuery, widget, dialog_manager, **kwargs):
    """Обработчик действий администратора"""
    await callback.answer("Функция в разработке")


main_window = Window(
    Format("{l10n_welcome}"),
    Group(
        Column(
            Button(
                Const("👥 Управление пользователями"),
                id="users_management",
                on_click=on_admin_action,
            ),
            Button(
                Const("📊 Статистика"),
                id="statistics",
                on_click=on_admin_action,
            ),
            Button(
                Const("⚙️ Настройки"),
                id="settings",
                on_click=on_admin_action,
            ),
        ),
        when="is_admin",
    ),
    Group(
        Column(
            GamesWindowWidgets.games_menu_button(),
            UserDialogWidgets.language_button(),
            UserDialogWidgets.support_button(),
        ),
        when=lambda data, case, manager: not data.get("is_admin", False),
    ),
    state=DuelSG.main_menu,
    getter=get_main_data,
)
