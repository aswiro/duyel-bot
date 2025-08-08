"""Базовые виджеты и кнопки для Aiogram Dialog."""

from aiogram_dialog.widgets.kbd import Button, SwitchTo, Start
from aiogram_dialog.widgets.text import Format
from .states import DuelSG


class BaseDialogWidgets:
    """Базовый класс для создания переиспользуемых виджетов диалогов."""

    @staticmethod
    def back_button(target_state, text_key: str = "back-to-menu"):
        """Создает кнопку возврата к указанному состоянию."""
        return SwitchTo(
            Format("{l10n_back}"),
            id="back",
            state=target_state,
        )

    @staticmethod
    def language_button():
        """Создает кнопку смены языка."""
        return SwitchTo(
            Format("{l10n_change_language}"),
            id="change_language",
            state=DuelSG.language_menu,
        )

    @staticmethod
    def custom_action_button(text_key: str, action_id: str, on_click_handler):
        """Создает кнопку с пользовательским обработчиком."""
        return Button(
            Format(f"{{l10n_{text_key}}}"),
            id=action_id,
            on_click=on_click_handler,
        )

    @staticmethod
    def support_button():
        """Создает кнопку поддержки."""
        return SwitchTo(
            Format("{l10n_support}"),
            id="support",
            state=DuelSG.support_menu,
        )


class AdminDialogWidgets(BaseDialogWidgets):
    """Виджеты для админских диалогов."""


class UserDialogWidgets(BaseDialogWidgets):
    """Виджеты для пользовательских диалогов."""


class GamesWindowWidgets(BaseDialogWidgets):
    """Виджеты для диалога игр."""

    @staticmethod
    def games_menu_button():
        """Создает кнопку меню игр."""
        return SwitchTo(
            Format("{l10n_games_menu}"),
            id="games",
            state=DuelSG.games_menu,
        )

    @staticmethod
    def my_games_button():
        """Создает кнопку моих игр."""
        return SwitchTo(
            Format("{l10n_my_games}"),
            id="my_games",
            state=DuelSG.my_games_menu,
        )

    @staticmethod
    def create_game_button():
        """Создает кнопку создания игры."""
        return Start(
            Format("{l10n_create_game}"),
            id="create_game",
            state=DuelSG.create_game,
        )
