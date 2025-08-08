"""Диалог игр."""

from datetime import datetime

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Column, Row, Select, SwitchTo
from aiogram_dialog.widgets.text import Format

from database import UnitOfWork
from database.models import GameStatusEnum
from handlers.widgets import GamesWindowWidgets
from utils import decimal_to_float, ensure_decimal

from ..constants import GAME_EMOJIS
from ..states import DuelSG


async def get_my_games_data(dialog_manager: DialogManager, **kwargs):
    """Получает данные для диалога "Мои игры"."""
    l10n = dialog_manager.middleware_data["l10n"]
    user_id = dialog_manager.event.from_user.id
    full_name = dialog_manager.event.from_user.full_name

    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    text = f"User {full_name} ({user_id}) is trying to get my games."
    async with uow:
        user = await uow.user_service.get_user(user_id, text)
        pending_games = await uow.game_service.get_user_games(
            user_id=user_id, status=GameStatusEnum.pending
        )

    # Словарь с эмодзи для каждого типа игры
    game_emojis = GAME_EMOJIS

    # Форматируем игры для отображения
    games_list = []
    for game in pending_games:
        game_type_str = game.game_type.value.capitalize()
        games_list.append(
            {
                "id": str(game.id),
                "name": f"#{game.id}",
                "stake": f"{decimal_to_float(game.stake_amount):.2f} USD.",
                "type_emoji": game_emojis.get(game.game_type, "❓"),
                "type_name": game_type_str,
            }
        )
    success_message = dialog_manager.dialog_data.get("success_message", None)
    has_success = False
    if success_message:
        has_success = True
    return {
        "has_success": has_success,
        "success_message": success_message,
        "games": games_list,
        "has_games": len(games_list) > 0,
        "balance": f"{decimal_to_float(user.balance):.2f}",
        "l10n_balance": l10n.format_value("balance"),
        "no-pending-games": l10n.format_value("no-pending-games"),
        "l10n_create_game": l10n.format_value("create-game"),
        "my_games_welcome": l10n.format_value(
            "my-games-welcome",
            {
                "user_name": full_name,
            },
        ),
        "games-list": l10n.format_value("games-list"),
        "l10n_back": l10n.format_value("back-to-menu"),
    }


async def on_back_to_games(
    callback: CallbackQuery, widget, dialog_manager: DialogManager
):
    """Удаляем сообщение об успехе, если оно есть"""
    if "success_message" in dialog_manager.dialog_data:
        del dialog_manager.dialog_data["success_message"]


async def on_create_game_click(
    callback: CallbackQuery, widget, dialog_manager: DialogManager
):
    """Обработчик нажатия на кнопку создания игры."""
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    user_id = callback.from_user.id

    async with uow:
        user = await uow.user_service.get_user(user_id)
        balance = decimal_to_float(user.balance) if user else 0
        
        # Проверяем количество активных игр пользователя
        games = await uow.game_service.get_user_games(
            user_id,
            GameStatusEnum.pending,
        )
        
    # Проверяем условия и перенаправляем на соответствующее окно
    if balance < 5.0:
        await dialog_manager.switch_to(DuelSG.insufficient_balance)
    elif len(games) >= 5:
        await dialog_manager.switch_to(DuelSG.max_games_reached)
    else:
        await dialog_manager.switch_to(DuelSG.create_game)


async def on_game_select(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str
):
    """Обработчик выбора игры."""
    l10n = dialog_manager.middleware_data["l10n"]
    uow: UnitOfWork = dialog_manager.middleware_data["uow"]
    game_id = int(item_id)

    async with uow:
        user = await uow.user_service.get_user(callback.from_user.id)
        game = await uow.game_service.get_game(game_id)
        stake = game.stake_amount
        balance = user.balance

        game_emoji = GAME_EMOJIS.get(game.game_type, "❓")
        new_balance = ensure_decimal(balance) + ensure_decimal(stake)
        await uow.user_service.update_user(user.id, {"balance": new_balance})
        await uow.game_service.update_game(
            game_id,
            {
                "status": GameStatusEnum.cancelled,
                "comment": f"User cancelled the game at {
                    datetime.now().strftime('%Y-%M-%D %H:%M:%S')
                }",
            },
        )
        await uow.commit()

    await callback.answer(
        text=l10n.format_value("game-cancelled", {"game_id": game_id}),
    )

    success_message = l10n.format_value(
        "game-deleted-success",
        {
            "game_emoji": game_emoji,
            "game_id": game.id,
            "stake": f"{decimal_to_float(game.stake_amount):.2f}",
            "balance": f"{decimal_to_float(new_balance):.2f}",
        },
    )
    dialog_manager.dialog_data["success_message"] = success_message

    await dialog_manager.switch_to(DuelSG.my_games_menu)


my_games_window = Window(
    Format("💰 {l10n_balance}: ${balance}"),
    Format(""),
    Format("{success_message}", when="success_message"),
    Format("{my_games_welcome}", when=~F["has_success"]),
    Format(""),
    Format("{games-list}:", when="has_games"),
    Column(
        Select(
            Format("{item[type_emoji]} {item[type_name]} #{item[id]} - {item[stake]}"),
            id="select_game",
            item_id_getter=lambda item: str(item["id"]),
            items="games",
            on_click=on_game_select,
        ),
        when="has_games",
    ),
    Format("{no-pending-games}", when=~F["has_games"]),
    Row(
        Button(
            Format("{l10n_create_game}"),
            id="create_game",
            on_click=on_create_game_click,
        ),
        SwitchTo(
            Format("{l10n_back}"),
            id="back_to_games",
            state=DuelSG.games_menu,
            on_click=on_back_to_games,
        ),
    ),
    getter=get_my_games_data,
    state=DuelSG.my_games_menu,
)
