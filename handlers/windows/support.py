"""Диалог поддержки."""

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Format

from ..states import DuelSG

from ..widgets import BaseDialogWidgets


async def get_support_data(dialog_manager: DialogManager, **kwargs):
    """Получает данные для диалога поддержки."""
    l10n = dialog_manager.middleware_data["l10n"]

    return {
        "l10n_support_title": l10n.format_value("support-title"),
        "l10n_contact_admin": l10n.format_value("contact-admin"),
        "l10n_faq": l10n.format_value("faq"),
        "l10n_back": l10n.format_value("back-to-menu"),
    }


async def on_contact_admin(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """Обработчик обращения к администратору."""
    l10n = dialog_manager.middleware_data["l10n"]
    await callback.answer(l10n.format_value("contact-admin-message"))


async def on_faq(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """Обработчик FAQ."""
    l10n = dialog_manager.middleware_data["l10n"]
    await callback.answer(l10n.format_value("faq-message"))


support_window = Window(
    Format("{l10n_support_title}"),
    Column(
        Button(
            Format("{l10n_contact_admin}"),
            id="contact_admin",
            on_click=on_contact_admin,
        ),
        Button(
            Format("{l10n_faq}"),
            id="faq",
            on_click=on_faq,
        ),
    ),
    BaseDialogWidgets.back_button(DuelSG.main_menu),
    state=DuelSG.support_menu,
    getter=get_support_data,
)
