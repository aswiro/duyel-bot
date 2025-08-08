"""Диалог игр."""

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Column, Group, Row, Select, SwitchTo
from aiogram_dialog.widgets.text import Format

from database import UnitOfWork
from database.models import GameStatusEnum, GameTypeEnum
from handlers.widgets import GamesWindowWidgets

from ..states import DuelSG

# Константы
GAME_EMOJIS = {
    GameTypeEnum.dice: "🎲",
    GameTypeEnum.darts: "🎯",
    GameTypeEnum.basketball: "🏀",
    GameTypeEnum.football: "⚽",
    GameTypeEnum.slot: "🎰",
    GameTypeEnum.bowling: "🎳",
}


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
                "stake": f"{game.stake_amount} USD.",
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
        "balance": float(user.balance),
        "l10n_balance": l10n.format_value("balance"),
        "no-pending-games": l10n.format_value("no-pending-games"),
        "l10n_create_game": l10n.format_value("create-game"),
        "my_games_welcome": l10n.format_value(
            "my-games-welcome", {"user_name": full_name, "balance": float(user.balance)}
        ),
        "my-games-list": l10n.format_value("my-games-list"),
        "l10n_back": l10n.format_value("back-to-menu"),
    }


async def on_back_to_games(
    callback: CallbackQuery, widget, dialog_manager: DialogManager
):
    """Удаляем сообщение об успехе, если оно есть"""
    if "success_message" in dialog_manager.dialog_data:
        del dialog_manager.dialog_data["success_message"]


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
        stake = float(game.stake_amount)
        balance = float(user.balance)

        game_emoji = GAME_EMOJIS.get(game.game_type, "❓")
        new_balance = balance + stake
        await uow.user_service.update_user(user.id, {"balance": new_balance})
        await uow.game_service.delete_game(game_id)
        await uow.commit()

    success_message = l10n.format_value(
        "game-deleted-success",
        {
            "game_emoji": game_emoji,
            "game_id": game.id,
            "stake": game.stake_amount,
            "balance": new_balance,
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
    Format("{my-games-list}:", when="has_games"),
    Group(
        Column(
            Select(
                Format(
                    "{item[type_emoji]} {item[type_name]} #{item[id]} - {item[stake]}"
                ),
                id="select_game",
                item_id_getter=lambda item: str(item["id"]),
                items="games",
                on_click=on_game_select,
            ),
        ),
        when="has_games",
    ),
    Format("{no-pending-games}", when=~F["has_games"]),
    Row(
        GamesWindowWidgets.create_game_button(),
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
