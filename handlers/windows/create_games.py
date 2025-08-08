"""Окна создания игр для Aiogram Dialog."""

from aiogram import F, types
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row
from aiogram_dialog.widgets.text import Format

from database import UnitOfWork
from database.models import GameStatusEnum, GameTypeEnum
from handlers.states import DuelSG
from handlers.widgets import BaseDialogWidgets


async def get_stake_data(dialog_manager: DialogManager, **kwargs):
    """Получает данные для ввода ставки и проверяет баланс пользователя."""
    l10n = dialog_manager.middleware_data["l10n"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    user_id = dialog_manager.event.from_user.id

    async with uow:
        user = await uow.user_service.get_user(user_id)
        balance = float(user.balance) if user else 0

    return {
        "balance": balance,
        "l10n_balance": l10n.format_value("balance"),
        "l10n_enter_stake": l10n.format_value("enter-stake"),
        "insufficient_balance": balance < 5.0,
        "l10n_insufficient_balance_message": l10n.format_value(
            "insufficient-balance-for-create"
        ),
        "l10n_back": l10n.format_value("back-to-menu"),
    }


async def on_stake_error(
    message: types.Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    """Обработчик ошибки ввода ставки."""
    l10n = dialog_manager.middleware_data["l10n"]
    await message.answer(l10n.format_value("invalid-stake-format"))


async def on_stake_success(
    message: types.Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    stake: float | int,
):
    """Обработчик успешного ввода ставки и создания игры."""
    l10n = dialog_manager.middleware_data["l10n"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    user_id = message.from_user.id
    if isinstance(stake, int):
        stake = float(stake)
    if stake <= 0.0:
        await message.answer(l10n.format_value("stake-must-be-positive"))
        return
    if stake < 5.0:
        success_message = l10n.format_value("stake-must-be-at-least-5")
        dialog_manager.dialog_data.update({"success_message": success_message})
        await dialog_manager.switch_to(DuelSG.my_games_menu)
        return
    if stake > 10000.0:
        await message.answer(l10n.format_value("stake-too-large"))
        return

    async with uow:
        user = await uow.user_service.get_user(user_id)
        game = await uow.game_service.get_user_games(
            user_id,
            GameStatusEnum.pending,
        )
        balance = float(user.balance) if user else 0

        if stake > balance:
            await message.answer(l10n.format_value("insufficient-balance-for-stake"))
            return
        if len(game) >= 5:
            success_message = l10n.format_value("max-games-reached")
            dialog_manager.dialog_data.update({"success_message": success_message})
            await dialog_manager.switch_to(DuelSG.my_games_menu)
            return
        game_emojis = {
            GameTypeEnum.dice: "🎲",
            GameTypeEnum.darts: "🎯",
            GameTypeEnum.basketball: "🏀",
            GameTypeEnum.football: "⚽",
            GameTypeEnum.slot: "🎰",
            GameTypeEnum.bowling: "🎳",
        }

        # Создаем игру сразу после успешного ввода ставки
        try:
            game_data = {
                "player1_id": user_id,
                "game_type": game_emojis.get(
                    GameTypeEnum.dice, "❓"
                ),  # По умолчанию dice
                "stake_amount": stake,
                "rolls_count": 3,  # По умолчанию 3
                "status": GameStatusEnum.pending,
            }

            await uow.game_service.create_game(game_data)
            new_balance = balance - stake
            await uow.user_service.update_user(user_id, {"balance": new_balance})
            await uow.commit()
            game_emoji = game_emojis.get(game_data["game_type"], "❓")
            success_message = l10n.format_value(
                "game-created-success",
                {
                    "game_emoji": game_emoji,
                    "game_type": str(game_data["game_type"]),
                    "stake": stake,
                    "rolls": game_data["rolls_count"],
                    "balance": new_balance,
                },
            )

            dialog_manager.dialog_data.update({"success_message": success_message})
            await dialog_manager.switch_to(DuelSG.my_games_menu)

        except Exception as e:
            await message.answer(l10n.format_value("game-creation-error"))
            print(f"Error creating game: {e}")


# Окно ввода ставки
create_game_window = Window(
    Format("💰 {l10n_balance}: ${balance}"),
    Format(""),
    # Сообщение о недостаточном балансе для создания игры
    Format("{l10n_insufficient_balance_message}", when=F["insufficient_balance"]),
    # Интерфейс для ввода ставки
    Format("{no_success_enter}", when="no_success"),
    Format("{l10n_enter_stake}", when=~F["insufficient_balance", "no_success"]),
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
