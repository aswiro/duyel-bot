"""Окна создания игр для Aiogram Dialog."""

from decimal import Decimal

from aiogram import F, types
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row
from aiogram_dialog.widgets.text import Format

from database import UnitOfWork
from database.models import GameStatusEnum, GameTypeEnum
from handlers.states import DuelSG
from handlers.widgets import BaseDialogWidgets
from utils import decimal_to_float, ensure_decimal

from ..constants import GAME_EMOJIS


async def on_stake_error(
    message: types.Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    """Обработчик ошибок ввода ставки."""
    l10n = dialog_manager.middleware_data["l10n"]

    # Устанавливаем флаг ошибки для отображения в интерфейсе
    dialog_manager.dialog_data["no_success"] = l10n.format_value("invalid-stake-format")


async def get_stake_data(dialog_manager: DialogManager, **kwargs):
    """Получает данные для ввода ставки."""
    l10n = dialog_manager.middleware_data["l10n"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    user_id = dialog_manager.event.from_user.id

    async with uow:
        user = await uow.user_service.get_user(user_id)
        balance = decimal_to_float(user.balance) if user else 0

    # Получаем сообщение об ошибке из dialog_data, если оно есть
    no_success_message = dialog_manager.dialog_data.get("no_success")

    return {
        "balance": balance,
        "l10n_balance": l10n.format_value("balance"),
        "l10n_enter_stake": l10n.format_value("enter-stake"),
        "l10n_back": l10n.format_value("back-to-menu"),
        "no_success": bool(no_success_message),
        "no_success_enter": no_success_message or "",
    }


async def get_insufficient_balance_data(dialog_manager: DialogManager, **kwargs):
    """Получает данные для окна с недостаточным балансом."""
    l10n = dialog_manager.middleware_data["l10n"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    user_id = dialog_manager.event.from_user.id

    async with uow:
        user = await uow.user_service.get_user(user_id)
        balance = decimal_to_float(user.balance) if user else 0

    return {
        "balance": balance,
        "l10n_balance": l10n.format_value("balance"),
        "l10n_insufficient_balance_message": l10n.format_value(
            "insufficient-balance-for-create"
        ),
        "l10n_back": l10n.format_value("back-to-menu"),
    }


async def get_max_games_data(dialog_manager: DialogManager, **kwargs):
    """Получает данные для окна с превышением лимита игр."""
    l10n = dialog_manager.middleware_data["l10n"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    user_id = dialog_manager.event.from_user.id

    async with uow:
        user = await uow.user_service.get_user(user_id)
        balance = decimal_to_float(user.balance) if user else 0

    return {
        "balance": balance,
        "l10n_balance": l10n.format_value("balance"),
        "l10n_max_games_message": l10n.format_value("max-games-reached"),
        "l10n_back": l10n.format_value("back-to-menu"),
    }


async def on_stake_success(
    message: types.Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    stake: float | int,
):
    """Обработчик успешного ввода ставки и создания игры."""
    # Очищаем сообщение об ошибке при успешном вводе
    if "no_success" in dialog_manager.dialog_data:
        del dialog_manager.dialog_data["no_success"]

    l10n = dialog_manager.middleware_data["l10n"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    user_id = message.from_user.id

    # Сначала проверяем количество активных игр
    async with uow:
        pending_games = await uow.game_service.get_user_games(
            user_id,
            GameStatusEnum.pending,
        )
        if len(pending_games) >= 5:
            dialog_manager.dialog_data["no_success"] = l10n.format_value(
                "max-games-reached"
            )
            return

    # Конвертируем stake в Decimal для точных вычислений
    stake_decimal = ensure_decimal(stake)

    if stake_decimal <= 0:
        dialog_manager.dialog_data["no_success"] = l10n.format_value(
            "stake-must-be-positive"
        )
        return
    if stake_decimal < 5:
        dialog_manager.dialog_data["no_success"] = l10n.format_value(
            "stake-must-be-at-least-5"
        )
        return
    if stake_decimal > 10000:
        dialog_manager.dialog_data["no_success"] = l10n.format_value("stake-too-large")
        return

    async with uow:
        user = await uow.user_service.get_user(user_id)
        game = await uow.game_service.get_user_games(
            user_id,
            GameStatusEnum.pending,
        )
        balance = user.balance if user else Decimal("0")

        if stake_decimal > balance:
            dialog_manager.dialog_data["no_success"] = l10n.format_value(
                "insufficient-balance-for-stake"
            )
            return

        bank_amount = stake_decimal * 2
        commission = bank_amount * Decimal("0.1")

        # Создаем игру сразу после успешного ввода ставки
        try:
            game_data = {
                "player1_id": user_id,
                "game_type": GameTypeEnum.dice,  # По умолчанию dice
                "stake_amount": stake_decimal,
                "bank_amount": bank_amount,
                "commission_amount": commission,
                "rolls_count": 3,  # По умолчанию 3
                "status": GameStatusEnum.pending,
            }

            await uow.game_service.create_game(game_data)
            new_balance = balance - stake_decimal
            await uow.user_service.update_user(user_id, {"balance": new_balance})
            await uow.commit()
            game_emoji = GAME_EMOJIS.get(game_data["game_type"], "❓")
            success_message = l10n.format_value(
                "game-created-success",
                {
                    "game_emoji": game_emoji,
                    "game_type": game_data["game_type"],
                    "stake": decimal_to_float(stake_decimal),
                    "rolls": game_data["rolls_count"],
                },
            )

            dialog_manager.dialog_data.update({"success_message": success_message})
            await dialog_manager.switch_to(DuelSG.my_games_menu)

        except Exception as e:
            await message.answer(l10n.format_value("game-creation-error"))
            print(f"Error creating game: {e}")


# Окно для недостаточного баланса
insufficient_balance_window = Window(
    Format("💰 {l10n_balance}: ${balance}"),
    Format(""),
    Format("{l10n_insufficient_balance_message}"),
    Row(
        BaseDialogWidgets.back_button(DuelSG.my_games_menu),
    ),
    state=DuelSG.insufficient_balance,
    getter=get_insufficient_balance_data,
)

# Окно для превышения лимита игр
max_games_window = Window(
    Format("💰 {l10n_balance}: ${balance}"),
    Format(""),
    Format("{l10n_max_games_message}"),
    Row(
        BaseDialogWidgets.back_button(DuelSG.my_games_menu),
    ),
    state=DuelSG.max_games_reached,
    getter=get_max_games_data,
)

# Окно ввода ставки
create_game_window = Window(
    Format("💰 {l10n_balance}: ${balance}"),
    Format(""),
    Format("{no_success_enter}", when="no_success"),
    Format("{l10n_enter_stake}"),
    TextInput(
        id="stake_input",
        type_factory=lambda x: int(x) if x.isdigit() else float(x),
        on_success=on_stake_success,
        on_error=on_stake_error,
    ),
    Row(
        BaseDialogWidgets.back_button(DuelSG.my_games_menu),
    ),
    state=DuelSG.create_game,
    getter=get_stake_data,
)
